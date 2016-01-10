# sync_mysql_databases
Compare the two MySQL databases(staging and production) and generate the sql file to patch the production database and make it same as staging database

## Description
- This is bit modified version of the http://code.activestate.com/recipes/576589-compare-mysql-db/. 
- In addition to the tables and table rows comparison, it tries to compare table structurs(DDL) as well.
- It considers the schenario of differences between the staging and production schema where production schema needs to be updated as per the staging schema.
- The output shows the three kind of differences:
	* If tables are identical in both the databases 
	* If table structures are identical in both the databases 
	* If rows in the tables are identical in both the databases
- The output SQL file is generated to patch the production schema to match it with stagin schema

## How to use the script

The script needs following arguments:
- staging database host
- staging database username
- staging database password
- staging database name
- production database host
- production database username
- production database password
- production database name
- and optional output file name (Default is production_patch.sql) 

You should pass the arguments in following way:

```
$ python mysql_db_sync.py 
Please provide all the required arguments.
USAGE:python dbcompare.py <staging_host> <staging_user> <staging_password> <staging_DB> <production_host> <production_user> <production_password> <production_DB> [<output filename>]
```


Sample Run:
```
$ time python dbcompare.py 127.0.0.1 user1 **** staging_database 127.0.0.1 user2 **** production_database
################## Check if number of tables are identical in both databases ###################
Number of tables in both the databases are not identical:
Following tables from DATABASE:staging_database missing in DATABASE:production_database
-> TABLE:table0


################## Check if table structures are identical in both databases ###################

TABLE:table1
STAGING DDL:
CREATE TABLE `table1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  `MARKS` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table1 is not identical in both the databases

TABLE:table2
STAGING DDL:
CREATE TABLE `table2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table2 is identical in both the databases

TABLE:table3
STAGING DDL:
CREATE TABLE `table3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table3 is identical in both the databases

TABLE:table4
STAGING DDL:
CREATE TABLE `table4` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table4` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table4 is identical in both the databases

TABLE:table5
STAGING DDL:
CREATE TABLE `table5` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table5` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table5 is identical in both the databases

TABLE:table6
STAGING DDL:
CREATE TABLE `table6` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table6` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table6 is identical in both the databases

TABLE:table7
STAGING DDL:
CREATE TABLE `table7` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table7` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table7 is identical in both the databases

TABLE:table8
STAGING DDL:
CREATE TABLE `table8` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table8` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table8 is identical in both the databases

TABLE:table9
STAGING DDL:
CREATE TABLE `table9` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

PRODUCTION DDL:
CREATE TABLE `table9` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=latin1;

-> Table structure of TABLE:table9 is identical in both the databases


################## Check if each table's rows are identical in both databases ###################

TABLE:table1
-> Rows in TABLE:table1 are not identical in both the databases
->-> 26 rows from production_database.table1 missing in staging_database.table1
->-> 26 rows from staging_database.table1 missing in production_database.table1

TABLE:table2
-> Rows in  TABLE:table2 are identical in both the databases

TABLE:table3
-> Rows in  TABLE:table3 are identical in both the databases

TABLE:table4
-> Rows in  TABLE:table4 are identical in both the databases

TABLE:table5
-> Rows in TABLE:table5 are not identical in both the databases
->-> 5 rows from staging_database.table5 missing in production_database.table5

TABLE:table6
-> Rows in  TABLE:table6 are identical in both the databases

TABLE:table7
-> Rows in  TABLE:table7 are identical in both the databases

TABLE:table8
-> Rows in  TABLE:table8 are identical in both the databases

TABLE:table9
-> Rows in  TABLE:table9 are identical in both the databases

real	0m0.333s
user	0m0.176s
sys	0m0.145s
```

## Limitations
- As in http://code.activestate.com/recipes/576589-compare-mysql-db/ this code as well uses the lists to store the table rows for comparioson and hence good for only small size databases.
- In case of structure differences in the tables it drops the older version from production and creates whole table from the scratch
- Not using bulk inserts and iserts are done row by row in the output sql file
