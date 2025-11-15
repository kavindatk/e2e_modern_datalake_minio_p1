# Building a Modern Lakehouse: End-to-End Data Engineering with MinIO, Hive, PySpark, Trino & DuckDB
<br/><br/>
<p align="center">
<picture>
  <img alt="docker" src="https://github.com/kavindatk/e2e_modern_datalake_minio_p1/blob/main/images/final_setup.JPG" width="800" height="300">
</picture>
</p>
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
<br/>

### Task 01 — Data Generation:
<br/>
A source program generates <b>customer transaction datasets every hour.</b>
<br/>

As I mentioned in the previous article, <b>we cannot use Hive directly through HUE</b> in this setup because we’ve modified the core architecture. Our focus here is only on the <b>Hive Metastore service.</b>
<br/>

During the <b>Data Generation</b> process, the data is uploaded to the <b>MinIO S3 bucket in a partitioned folder</b> structure (organized by date and hour).
To make the data easier to view and manage, I’ll create a Hive table for these files using Beeline.
<br/>

For this step, I’ll log in to <b>VM1 (where Beeline is installed)</b>, create the Hive table, and load the data into the corresponding partitions.
<br/><br/>

#### The data loading and table creation process is shown below.

<br/>

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
```

<br/><br/>
### Task 02 — Transformation & Compression:

Spark processes and compresses these files, then stores them as Iceberg tables in MinIO.
<br/><br/>

In this task, I will perform transformations on the data and save the results into an <b>Iceberg table</b> using <b>PySpark</b>. During this process, the data will be written in <b>Parquet</b> format with <b>Snappy compression.</b>
For this job, I’m using <b>VM1</b>, which currently functions as the <b>Spark master node.</b> The transformation job runs as a cron job, where it reads <b>H-2 (two hours old)</b> data every hour and writes the transformed output to the MinIO bucket.

Since my Spark cluster is also running in Docker containers, I use a <b>shell script</b> to automate the execution of the PySpark job. The script also writes logs, which can be used later for auditing and troubleshooting.
Additionally, you can view each executed instance in the Spark Web UI within its respective time window.

Both the PySpark code and the shell script are uploaded to the <b>Data Transformation folder</b> referenced above.
<br/>

```bash
0: jdbc:hive2:///> use my_db;
No rows affected (0.036 seconds)
0: jdbc:hive2:///> show tables;
+----------------+
|    tab_name    |
+----------------+
| customer_data  |
+----------------+
1 row selected (0.068 seconds)
0: jdbc:hive2:///> describe formatted customer_data;
+-------------------------------+----------------------------------------------------+----------------------------------------------------+
|           col_name            |                     data_type                      |                      comment                       |
+-------------------------------+----------------------------------------------------+----------------------------------------------------+
| name                          | string                                             |                                                    |
| address                       | string                                             |                                                    |
| city                          | string                                             |                                                    |
| country                       | string                                             |                                                    |
| job                           | string                                             |                                                    |
| passport_number               | string                                             |                                                    |
| date_of_birth                 | date                                               |                                                    |
| transction_date               | date                                               |                                                    |
| purchase_units                | int                                                |                                                    |
| discount_percentage           | decimal(5,2)                                       |                                                    |
| transction_amount             | decimal(10,2)                                      |                                                    |
| dateval                       | string                                             |                                                    |
|                               | NULL                                               | NULL                                               |
| # Detailed Table Information  | NULL                                               | NULL                                               |
| Database:                     | my_db                                              | NULL                                               |
| OwnerType:                    | USER                                               | NULL                                               |
| Owner:                        | spark                                              | NULL                                               |
| CreateTime:                   | Sat Nov 15 08:50:40 UTC 2025                       | NULL                                               |
| LastAccessTime:               | Mon Dec 08 10:44:42 UTC 1969                       | NULL                                               |
| Retention:                    | 2147483647                                         | NULL                                               |
| Location:                     | s3a://warehouse/tablespace/external_tables/my_db.db/customer_data | NULL                                               |
| Table Type:                   | EXTERNAL_TABLE                                     | NULL                                               |
| Table Parameters:             | NULL                                               | NULL                                               |
|                               | DO_NOT_UPDATE_STATS                                | true                                               |
|                               | EXTERNAL                                           | TRUE                                               |
|                               | current-schema                                     | {\"type\":\"struct\",\"schema-id\":0,\"fields\":[{\"id\":1,\"name\":\"name\",\"required\":false,\"type\":\"string\"},{\"id\":2,\"name\":\"address\",\"required\":false,\"type\":\"string\"},{\"id\":3,\"name\":\"city\",\"required\":false,\"type\":\"string\"},{\"id\":4,\"name\":\"country\",\"required\":false,\"type\":\"string\"},{\"id\":5,\"name\":\"job\",\"required\":false,\"type\":\"string\"},{\"id\":6,\"name\":\"passport_number\",\"required\":false,\"type\":\"string\"},{\"id\":7,\"name\":\"date_of_birth\",\"required\":false,\"type\":\"date\"},{\"id\":8,\"name\":\"transction_date\",\"required\":false,\"type\":\"date\"},{\"id\":9,\"name\":\"purchase_units\",\"required\":false,\"type\":\"int\"},{\"id\":10,\"name\":\"discount_percentage\",\"required\":false,\"type\":\"decimal(5, 2)\"},{\"id\":11,\"name\":\"transction_amount\",\"required\":false,\"type\":\"decimal(10, 2)\"},{\"id\":12,\"name\":\"dateval\",\"required\":false,\"type\":\"string\"}]} |
|                               | current-snapshot-id                                | 2861418859086358860                                |
|                               | current-snapshot-summary                           | {\"spark.app.id\":\"app-20251115161006-0024\",\"added-data-files\":\"1\",\"added-records\":\"600000\",\"added-files-size\":\"38728757\",\"changed-partition-count\":\"1\",\"total-records\":\"600000\",\"total-files-size\":\"38728757\",\"total-data-files\":\"1\",\"total-delete-files\":\"0\",\"total-position-deletes\":\"0\",\"total-equality-deletes\":\"0\",\"engine-version\":\"4.0.0\",\"app-id\":\"app-20251115161006-0024\",\"engine-name\":\"spark\",\"iceberg-version\":\"Apache Iceberg 1.10.0 (commit 2114bf631e49af532d66e2ce148ee49dd1dd1f1f)\"} |
|                               | current-snapshot-timestamp-ms                      | 1763223043270                                      |
|                               | default-partition-spec                             | {\"spec-id\":0,\"fields\":[{\"name\":\"dateval\",\"transform\":\"identity\",\"source-id\":12,\"field-id\":1000}]} |
|                               | metadata_location                                  | s3a://warehouse/tablespace/external_tables/my_db.db/customer_data/metadata/00008-86f4b75b-2f70-4d5f-8d82-a9f238d7ab01.metadata.json |
|                               | numFiles                                           | 1                                                  |
|                               | numRows                                            | 600000                                             |
|                               | owner                                              | spark                                              |
|                               | previous_metadata_location                         | s3a://warehouse/tablespace/external_tables/my_db.db/customer_data/metadata/00007-8fe0da66-47ea-4383-a716-4da38856a4b9.metadata.json |
|                               | snapshot-count                                     | 9                                                  |
|                               | table_type                                         | ICEBERG                                            |
|                               | totalSize                                          | 38728757                                           |
|                               | transient_lastDdlTime                              | 1763196640                                         |
|                               | uuid                                               | 9ca1cef7-d118-4f24-803a-161f5aaa1b68               |
|                               | write.format.default                               | parquet                                            |
|                               | write.parquet.compression-codec                    | snappy                                             |
|                               | NULL                                               | NULL                                               |
| # Storage Information         | NULL                                               | NULL                                               |
| SerDe Library:                | org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe | NULL                                               |
| InputFormat:                  | org.apache.hadoop.mapred.FileInputFormat           | NULL                                               |
| OutputFormat:                 | org.apache.hadoop.mapred.FileOutputFormat          | NULL                                               |
| Compressed:                   | No                                                 | NULL                                               |
| Num Buckets:                  | 0                                                  | NULL                                               |
| Bucket Columns:               | []                                                 | NULL                                               |
| Sort Columns:                 | []                                                 | NULL                                               |
+-------------------------------+----------------------------------------------------+----------------------------------------------------+
51 rows selected (0.266 seconds)


```

<br/><br/>


### Task 03 — Querying with Trino (via Hue):

Use Hue to run SQL queries through Trino for fast, interactive analytics.
<br/><br/>

Now it’s time to test the work we’ve done so far.
The Spark job is running smoothly and successfully loading data into the <b>Iceberg table.</b>
Next, we will run some queries to validate the data.

For querying, my primary tool is <b>Trino</b>, which is already integrated with <b>HUE</b>. Using HUE, I can run interactive SQL queries directly on the Iceberg table.
In addition to Trino queries, I will also show examples of executing the same queries using <b>Spark SQL</b>, so you can compare both approaches.

Below are some sample queries executed using <b>Trino and Spark SQL.</b>
<br/>

#### Trino

```sql
#Trino  Catalog should be "iceberg"

SELECT * FROM iceberg.my_db.customer_data;

SELECT count(*) FROM iceberg.my_db.customer_data;
```

<br/><br/>

#### Spark SQL

```sql
#Trino  Catalog should be "iceberg_catalog"

SELECT * FROM iceberg_catalog.my_db.customer_data;

SELECT count(*) FROM iceberg_catalog.my_db.customer_data;

```
<br/>
#### Useful Iceberg commands for Spark SQL

```sql
# Check Snapshots

SELECT * FROM iceberg_catalog.my_db.customer_data.snapshots;

# Iceberg metadata snapshots ,history ,files ,manifests

SELECT * FROM iceberg_catalog.my_db.customer_data.history;
SELECT * FROM iceberg_catalog.my_db.customer_data.files;

# Describer Table

DESCRIBE TABLE iceberg_catalog.my_db.customer_data;

#  Query by snapshot ID or Timestamp

SELECT * FROM iceberg_catalog.my_db.customer_data VERSION AS OF <snapshot id>;

SELECT * FROM iceberg_catalog.my_db.customer_data TIMESTAMP AS OF <timestamp>;

```

<br/><br/>

<br/><br/>
### Task 04 — Loading Data into DuckDB:

Load and query the same processed data directly from DuckDB for lightweight local analytics.
<br/><br/>
Finally, I will demonstrate how to read the processed Iceberg data using <b>DuckDB</b>, which operates as a separate component in our architecture.
DuckDB is rapidly gaining popularity in the industry due to its ability to handle heavy analytical workloads with impressive, Spark-like performance — all while running locally with minimal setup.

The following steps show how DuckDB connects to MinIO, reads the Iceberg/Parquet data, and performs fast analytical queries.
<br/><br/>

```xml
# Persistent Database creating code

.open /home/hadoop/duckdb_test/customer_data.db

INSTALL httpfs;
LOAD httpfs;

-- MinIO S3 configuration
SET s3_endpoint='minoproxy:9999';
SET s3_access_key_id='minioadmin';
SET s3_secret_access_key='minioadmin';
SET s3_region='us-east-1';
SET s3_url_style='path';
SET s3_use_ssl=false;



-- Create a view from the MINIO data files

CREATE VIEW customer_data AS
SELECT * FROM read_parquet('s3://warehouse/tablespace/external_tables/my_db.db/customer_data/data/dateval=*/*.parquet');


.quit
```

<br/><br/>

```bash
# Create Duckdb persistent database

hadoop@node01:~/duckdb_test$ duckdb
DuckDB v1.4.1 (Andium) b390a7c376
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
D
D .open /home/hadoop/duckdb_test/customer_data.db
D
D INSTALL httpfs;
D LOAD httpfs;
D
D -- MinIO S3 configuration
D SET s3_endpoint='minoproxy:9999';
D SET s3_access_key_id='minioadmin';
D SET s3_secret_access_key='minioadmin';
D SET s3_region='us-east-1';
D SET s3_url_style='path';
D SET s3_use_ssl=false;
D
D
D
D -- Create a view from the MINIO data files
D
D
D CREATE VIEW customer_data AS
  SELECT * FROM read_parquet('s3://warehouse/tablespace/external_tables/my_db.db/customer_data/data/dateval=*/*.parquet');
D
D .quit
hadoop@node01:~/duckdb_test$
```

<br/><br/>

```bash
# Testing  DuckDb data

hadoop@node01:~/duckdb_test$ ls
customer_data.db  duck.txt  sparkdb.db
hadoop@node01:~/duckdb_test$
hadoop@node01:~/duckdb_test$ duckdb customer_data.db
DuckDB v1.4.1 (Andium) b390a7c376
Enter ".help" for usage hints.
D show tables;
┌───────────────┐
│     name      │
│    varchar    │
├───────────────┤
│ customer_data │
└───────────────┘
D select * from customer_data limit 10;
┌─────────────────────┬──────────────────────┬──────────────────┬────────────┬───┬────────────────┬─────────────────────┬───────────────────┬────────────┐
│        name         │       address        │       city       │  country   │ … │ purchase_units │ discount_percentage │ transction_amount │  dateval   │
│       varchar       │       varchar        │     varchar      │  varchar   │   │     int32      │    decimal(5,2)     │   decimal(10,2)   │    date    │
├─────────────────────┼──────────────────────┼──────────────────┼────────────┼───┼────────────────┼─────────────────────┼───────────────────┼────────────┤
│ Denise Williams     │ 5915 Elliott Neck …  │ Bellton          │ Bahrain    │ … │             37 │               10.00 │             81.55 │ 2025-11-15 │
│ Alyssa Burgess      │ 89760 Collins Vill…  │ West Michael     │ Kazakhstan │ … │             12 │               13.00 │             34.66 │ 2025-11-15 │
│ Elizabeth Jones     │ 507 Joshua Ports S…  │ Lake Jessica     │ Gibraltar  │ … │             52 │                7.00 │             47.88 │ 2025-11-15 │
│ Peter Jackson       │ 87063 Young Turnpi…  │ Samuelborough    │ Guyana     │ … │             25 │               16.00 │             92.37 │ 2025-11-15 │
│ Joshua Hall         │ 6713 Jill Bridge, …  │ Natalieville     │ Djibouti   │ … │             65 │               16.00 │             10.73 │ 2025-11-15 │
│ Christopher Stewart │ 1373 Wolf Avenue, …  │ Lake Jennifer    │ Italy      │ … │             26 │               24.00 │             42.15 │ 2025-11-15 │
│ Nicole Carroll      │ 191 Angela Mountai…  │ Codymouth        │ Guernsey   │ … │             71 │               20.00 │             45.75 │ 2025-11-15 │
│ Jacqueline Brooks   │ 7785 Jones Pass Ap…  │ Noahfort         │ Tajikistan │ … │             42 │               18.00 │             98.45 │ 2025-11-15 │
│ Justin Dyer         │ 04089 Wyatt Mounta…  │ New Heatherville │ Belize     │ … │             55 │                3.00 │             79.62 │ 2025-11-15 │
│ Christy Campbell    │ 49458 Edward Inlet…  │ Port Jonathan    │ Botswana   │ … │             45 │                7.00 │             53.56 │ 2025-11-15 │
├─────────────────────┴──────────────────────┴──────────────────┴────────────┴───┴────────────────┴─────────────────────┴───────────────────┴────────────┤
│ 10 rows                                                                                                                           12 columns (8 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
D
D select count(*) from customer_data ;
┌────────────────┐
│  count_star()  │
│     int64      │
├────────────────┤
│    1200000     │
│ (1.20 million) │
└────────────────┘
D .quit
hadoop@node01:~/duckdb_test$

```

