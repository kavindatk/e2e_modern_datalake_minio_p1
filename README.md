# Building a Modern Lakehouse: End-to-End Data Engineering with MinIO, Hive, PySpark, Trino & DuckDB
<br/><br/>
## 🚀 Building a Complete End-to-End Data Engineering Pipeline
<br/><br/>
We’ve now built a <b>modern data lakehouse</b> that brings together several powerful open-source technologies.
Our architecture uses <b>MinIO (S3-compatible object storage)</b> as the foundation, with <b>Hive Metastore</b> managing metadata and <b>Apache Iceberg</b> providing an advanced table format.
<br/>
<b>Apache Spark</b> powers large-scale data processing, while <b>Hue</b> offers an interactive GUI interface for <b>Trino</b> and <b>Spark SQL</b>, making SQL querying fast and intuitive.
Finally, <b>DuckDB</b> delivers ultra-fast local analytics directly on top of the same data.
<br/>
Now, it’s time to implement a <b>complete end-to-end data engineering pipeline</b> using this setup.
<br/><br/>


## 🔄 Workflow Summary
<br/><br/>

### Task 01 — Data Generation:

A source program generates <b>customer transaction datasets every hour.</b>
<br/>

As I mentioned in the previous article, <b>we cannot use Hive directly through HUE</b> in this setup because we’ve modified the core architecture. Our focus here is only on the <b>Hive Metastore service.</b>
<br/>

During the <b>Data Generation</b> process, the data is uploaded to the <b>MinIO S3 bucket in a partitioned folder</b> structure (organized by date and hour).
To make the data easier to view and manage, I’ll create a Hive table for these files using Beeline.
<br/>

For this step, I’ll log in to <b>VM1 (where Beeline is installed)</b>, create the Hive table, and load the data into the corresponding partitions.
<br/>

#### The data loading and table creation process is shown below.

```bash
hadoop@node01:~$  docker exec -it hive_server2 beeline -u "jdbc:hive2:///"
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/opt/hive/lib/log4j-slf4j-impl-2.18.0.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-reload4j-1.7.36.jar!/org/slf4j/impl/StaticLoggerBinder.class]
Connecting to jdbc:hive2:///
25/11/13 16:15:43 [main]: WARN conf.HiveConf: HiveConf of name hive.default.table.type does not exist
Hive Session ID = 2d99422f-4edd-44d5-af8b-90f28032fcce
25/11/13 16:15:48 [main]: WARN session.SessionState: Configuration hive.reloadable.aux.jars.path not specified
Connected to: Apache Hive (version 4.0.0)
Driver: Hive JDBC (version 4.0.0)
Transaction isolation: TRANSACTION_REPEATABLE_READ
Beeline version 4.0.0 by Apache Hive
0: jdbc:hive2:///> show databases;
25/11/13 16:18:23 [Metastore-RuntimeStats-Loader-1]: WARN conf.HiveConf: HiveConf of name hive.default.table.type does not exist
+----------------+
| database_name  |
+----------------+
| customer_info  |
| default        |
| hivedb         |
+----------------+
3 rows selected (2.466 seconds)
0: jdbc:hive2:///> use customer_info;
No rows affected (0.038 seconds)
0: jdbc:hive2:///>
0: jdbc:hive2:///>
0: jdbc:hive2:///>
0: jdbc:hive2:///> CREATE EXTERNAL TABLE IF NOT EXISTS customer_info.customer_data (
. . . . . . . . .>     name STRING,
. . . . . . . . .>     address STRING,
. . . . . . . . .>     city STRING,
. . . . . . . . .>     country STRING,
. . . . . . . . .>     job STRING,
. . . . . . . . .>     passport_number STRING,
. . . . . . . . .>     date_of_birth STRING,
. . . . . . . . .>     entry_date STRING,
. . . . . . . . .>     entry_time STRING,
. . . . . . . . .>     random_number BIGINT
. . . . . . . . .> )
. . . . . . . . .> PARTITIONED BY (
. . . . . . . . .>     dateval STRING,
. . . . . . . . .>     hourval STRING
. . . . . . . . .> )
. . . . . . . . .> ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
. . . . . . . . .> WITH SERDEPROPERTIES (
. . . . . . . . .>     "separatorChar" = ",",
. . . . . . . . .>     "quoteChar" = "\"",
. . . . . . . . .>     "escapeChar" = "\\"
. . . . . . . . .> )
. . . . . . . . .> STORED AS TEXTFILE
. . . . . . . . .> LOCATION 's3a://cusdatabucket/customer_data/'
. . . . . . . . .> TBLPROPERTIES ("skip.header.line.count"="1");
No rows affected (0.12 seconds)
0: jdbc:hive2:///>
0: jdbc:hive2:///> MSCK REPAIR TABLE customer_data;
No rows affected (0.508 seconds)
0: jdbc:hive2:///>
0: jdbc:hive2:///> select * from customer_info.customer_data limit 10;
25/11/13 16:52:22 [a04f1ff2-0a7b-4444-a305-8db74af930d1 main]: WARN calcite.RelOptHiveTable: No Stats for customer_info@customer_data, Columns: country, entry_time, address, city, date_of_birth, passport_number, random_number, name, job, entry_date
No Stats for customer_info@customer_data, Columns: country, entry_time, address, city, date_of_birth, passport_number, random_number, name, job, entry_date
25/11/13 16:52:22 [a04f1ff2-0a7b-4444-a305-8db74af930d1 main]: WARN optimizer.SimpleFetchOptimizer: Table customer_info@customer_data is external table, falling back to filesystem scan.
+---------------------+----------------------------------------------------+---------------------+----------------------------+----------------------------------------+--------------------------------+------------------------------+---------------------------+---------------------------+------------------------------+------------------------+------------------------+
| customer_data.name  |               customer_data.address                | customer_data.city  |   customer_data.country    |           customer_data.job            | customer_data.passport_number  | customer_data.date_of_birth  | customer_data.entry_date  | customer_data.entry_time  | customer_data.random_number  | customer_data.dateval  | customer_data.hourval  |
+---------------------+----------------------------------------------------+---------------------+----------------------------+----------------------------------------+--------------------------------+------------------------------+---------------------------+---------------------------+------------------------------+------------------------+------------------------+
| Tyler Odom          | USS Harris, FPO AE 22339                           | West Aliciabury     | United Kingdom             | Emergency planning/management officer  | 496976522                      | 2021-01-17                   | 20251113                  | 000601                    | 4527                         | 20251113               | 00                     |
| Kevin Jones         | 353 Cain Hollow, New Keith, MT 13057               | Lake Kyle           | Dominica                   | Administrator, sports                  | 131234885                      | 1922-08-14                   | 20251113                  | 000601                    | 6781                         | 20251113               | 00                     |
| Matthew Snyder      | 12784 Tyler Glens Suite 379, East Shirleymouth, RI 77636 | Lake Kayleemouth    | Suriname                   | Producer, radio                        | G27771783                      | 1954-06-26                   | 20251113                  | 000601                    | 8188                         | 20251113               | 00                     |
| John Gibson         | 635 Paul Drives, Lake Christopherside, AR 05657    | East Barryhaven     | Panama                     | Medical secretary                      | 424373362                      | 2007-03-12                   | 20251113                  | 000601                    | 8239                         | 20251113               | 00                     |
| Theresa Clark       | 0669 Norris Radial Suite 123, Calebland, OR 25226  | Allenstad           | Latvia                     | Education officer, community           | 124258949                      | 1919-06-17                   | 20251113                  | 000601                    | 5124                         | 20251113               | 00                     |
| Maureen Jackson     | 3475 Castillo Motorway, North Anthonytown, OR 88168 | Cindyburgh          | Saint Pierre and Miquelon  | Optometrist                            | H81637693                      | 2025-05-11                   | 20251113                  | 000601                    | 4138                         | 20251113               | 00                     |
| Mr. Robert Johnson  | Unit 2884 Box 5886, DPO AP 05107                   | North Travis        | Uzbekistan                 | Education administrator                | S29043044                      | 1933-02-19                   | 20251113                  | 000601                    | 7654                         | 20251113               | 00                     |
| Sarah Davis         | 12841 Alexander Divide Suite 923, North Richardfurt, GA 91592 | West John           | Iran                       | Ergonomist                             | R11913124                      | 2023-12-05                   | 20251113                  | 000601                    | 4152                         | 20251113               | 00                     |
| Tamara Simpson      | 440 Davis Street Apt. 715, South Jasminemouth, NH 76878 | New Patrickmouth    | Rwanda                     | Translator                             | A10385761                      | 1951-12-30                   | 20251113                  | 000601                    | 2434                         | 20251113               | 00                     |
| Debra Adams         | 0989 Koch Way Apt. 311, Mistyshire, WY 65315       | Derekport           | Malta                      | Visual merchandiser                    | P15426544                      | 1914-09-10                   | 20251113                  | 000601                    | 4452                         | 20251113               | 00                     |
+---------------------+----------------------------------------------------+---------------------+----------------------------+----------------------------------------+--------------------------------+------------------------------+---------------------------+---------------------------+------------------------------+------------------------+------------------------+
10 rows selected (0.608 seconds)
0: jdbc:hive2:///>
0: jdbc:hive2:///>
```

<br/><br/>
### Task 02 — Transformation & Compression:

Spark processes and compresses these files, then stores them as Iceberg tables in MinIO.
<br/><br/>
### Task 03 — Querying with Trino (via Hue):

Use Hue to run SQL queries through Trino for fast, interactive analytics.
<br/><br/>
### Task 04 — Loading Data into DuckDB:

Load and query the same processed data directly from DuckDB for lightweight local analytics.
