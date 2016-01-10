import os, os.path, MySQLdb, pprint, string, sys

class params(object):
    """ Class used to store global parameters
    """
    # Connection parameters to the DB we want to compare
    def __init__(self, stagingDB_params, productionDB_params, outfile):
        # DB 1
        self.stagingDB_params=stagingDB_params
        self.stagingDB=MySQLdb.connect(stagingDB_params["host"], stagingDB_params["user"], stagingDB_params["passwd"], stagingDB_params["db"])
        # DB 2
        self.productionDB_params=productionDB_params
        self.productionDB=MySQLdb.connect(productionDB_params["host"], productionDB_params["user"], productionDB_params["passwd"], productionDB_params["db"])
        # Output file to store the patch need to be applied
        self.outfile=outfile

class dbUtils(object):
    """ Utilities to interact with database
    """
    def __init__(self, db, name=''):
        self.db=db
        self.name=name
        self.cur=db.cursor()

    def rowmap(self, rows):
        """ returns a dictionary with column names as keys and values
        """
        cols = [column[0] for column in self.cur.description]
        return [dict(zip(cols, row)) for row in rows]

    def getRows(self, tbl):
        """ Returns the content of the table tbl
        """
        statmt="select * from %s" % tbl
        self.cur.execute(statmt)
        rows=list(self.cur.fetchall())
        return rows

    def getTableList(self):
        """ Returns the list of the DB tables
        """
        statmt="show tables"
        self.cur.execute(statmt)
        rows=list(self.cur.fetchall())
        return rows
    
    def getTableCreateStatement(self, table_name):
        """ Returns the DDL for table
        """
        statmt="SHOW CREATE TABLE %s" % table_name
        self.cur.execute(statmt)
        row = self.cur.fetchone()
        return row[1] + ';\n'

class dbCompare(object):
    """ Core function to compare the DBs
    """
    def __init__(self, prms):
        self.prms = prms

    def compareLists(self, l1, l2):
        result={'l1notInl2':[],
                'l2notInl1':[]}
        d1=dict(zip(l1, l1))
        d2=dict(zip(l2, l2))
        for row in l1:
            if not d2.has_key(row):
                result['l1notInl2'].append(row)
        for row in l2:
            if not d1.has_key(row):
                result['l2notInl1'].append(row)
        return result

    def process(self):
        of=outFile(self.prms.outfile)
        stagingDB=dbUtils(self.prms.stagingDB, self.prms.stagingDB_params["db"])
        tl1=stagingDB.getTableList()
        # 
        productionDB=dbUtils(self.prms.productionDB, self.prms.productionDB_params["db"])
        tl2=productionDB.getTableList()
        
        print "################## Check if number of tables are identical in both databases ###################"
        if tl1==tl2:
            print "Number of tables in both the databases are identical"
        else:
            print "Number of tables in both the databases are not identical:"
            cp=self.compareLists(tl1, tl2)
            if cp['l1notInl2'] != []:
                print "Following tables from DATABASE:%s missing in DATABASE:%s" % (stagingDB.name, productionDB.name)
                print string.join(['-> TABLE:' + t[0] for t in cp['l1notInl2']],'\n')
                for tbl in cp['l1notInl2']:
                    #Create the missing table
                    of.write("-- Creating the missing TABLE:%s from staging database" % tbl)
                    of.write(stagingDB.getTableCreateStatement(tbl))
                    
                    #Populate the table from staging database
                    of.write("-- Populating the missing TABLE:%s from staging database" % tbl)
                    tbl_rows=stagingDB.getRows(tbl)
                    for row in stagingDB.rowmap(tbl_rows):
                        insert_stmt = "INSERT INTO `%s`(%s) VALUES(%s);\n"%(tbl[0], ",".join(["`"+key+"`" for key in row.keys()]), ",".join(["'"+str(value)+"'" if value is not None else 'NULL' for value in row.values()]))
                        of.write(insert_stmt)
                                    
            if cp['l2notInl1'] != []:
                print "Following tables from %s missing in %s" % (productionDB.name, stagingDB.name)
                print string.join([t[0] for t in cp['l2notInl1']], '\n')
                for tbl in cp['l2notInl1']:
                    #Drop the extra table
                    of.write("-- Dropping the TABLE:%s from production database" % tbl)
                    drop_table_stmt = "DROP TABLE `%s`;\n" % tbl
                    of.write(drop_table_stmt)
                    
        print "\n\n################## Check if table structures are identical in both databases ###################"
        for tbl in tl1:
            if tbl in tl2:
                print '\nTABLE:' + tbl[0]
                ddl1=stagingDB.getTableCreateStatement(tbl)
                ddl2=productionDB.getTableCreateStatement(tbl)
                print "STAGING DDL:\n"+ddl1
                print "PRODUCTION DDL:\n"+ddl2
                if ddl1==ddl2:
                    print "-> Table structure of TABLE:%s is identical in both the databases" % tbl
                else:
                    print "-> Table structure of TABLE:%s is not identical in both the databases" % tbl
                    #Drop the current table from the production
                    of.write("-- Dropping the old structured TABLE:%s from production database" % tbl)
                    drop_table_stmt = "DROP TABLE `%s`;\n" % tbl
                    of.write(drop_table_stmt)
                    
                    #Create the table as per definition from staging schema
                    of.write("-- Creating the new structured TABLE:%s from staging database" % tbl)
                    of.write(stagingDB.getTableCreateStatement(tbl))
                    
                    #Populate the table from staging database
                    #This will be taken care by 3rd case ie if rows are different

                    
        print "\n\n################## Check if each table's rows are identical in both databases ###################"
        for tbl in tl1:
            if tbl in tl2:
                print '\nTABLE:' + tbl[0]
                rl1=stagingDB.getRows(tbl)
                rl2=productionDB.getRows(tbl)
                if rl1==rl2:
                    print "-> Rows in  TABLE:%s are identical in both the databases" % tbl
                else:
                    print "-> Rows in TABLE:%s are not identical in both the databases" % tbl
                    cp=self.compareLists(rl1, rl2)
                    if cp['l2notInl1'] != []:
                        print "->-> %d rows from %s.%s missing in %s.%s" % (len(cp['l2notInl1']), productionDB.name, tbl[0], stagingDB.name, tbl[0])
                        #Drop the extra rows from production database
                        of.write("-- Dropping the extra rows from TABLE:%s from production database" % tbl)
                        for row in productionDB.rowmap(cp['l2notInl1']):
                            where_clause = ' AND '.join(["`"+key+"` = '"+str(value)+"'"  if value is not None else "`"+key+"` IS NULL" for key, value in row.iteritems()])
                            delete_stmt = "DELETE FROM `%s` WHERE %s;\n"%(tbl[0],where_clause)
                            of.write(delete_stmt)
                    if cp['l1notInl2'] != []:
                        print "->-> %d rows from %s.%s missing in %s.%s" % (len(cp['l1notInl2']), stagingDB.name, tbl[0], productionDB.name, tbl[0])
                        #Insert the missing rows
                        of.write("-- Inserting the missing rows in TABLE:%s from staging database" % tbl)
                        for row in stagingDB.rowmap(cp['l1notInl2']):
                            insert_stmt = "INSERT INTO `%s`(%s) VALUES(%s);\n"%(tbl[0], ",".join(["`"+key+"`" for key in row.keys()]), ",".join(["'"+str(value)+"'" if value is not None else 'NULL' for value in row.values()]))
                            of.write(insert_stmt)
                    
                                
class outFile(object):
    """ To write in the output file
    """
    def __init__(self, outfile):
        self.outFile=outfile
        df=open(self.outFile,'w')
        df.close()

    def write(self, *msg):
        df=open(self.outFile,'a')
        for m in msg:
                df.write("%s\n" % str(m))
        df.close()

if __name__ == "__main__":
    if len(sys.argv)<9:
        usage="Please provide all the required arguments.\n"\
               "USAGE:python dbcompare.py <staging_host> <staging_user> <staging_password> <staging_DB> <production_host> <production_user> <production_password> <production_DB> [<output filename>]"
        print usage
        exit(1)
    else:
        stagingDB_params={"host": sys.argv[1], "user":sys.argv[2], "passwd":sys.argv[3], "db":sys.argv[4]}
        productionDB_params={"host": sys.argv[5], "user":sys.argv[6], "passwd":sys.argv[7], "db":sys.argv[8]}
        
    if len(sys.argv)>9:
        outfile=sys.argv[9]
    else:
        outfile='production_patch.sql'
    prms = params(stagingDB_params, productionDB_params, outfile)
    dc=dbCompare(prms)
    dc.process()
