# Building a Modern Lakehouse: End-to-End Data Engineering with MinIO, Hive, PySpark, Trino & DuckDB
<br/><br/>
## 🚀 Building a Complete End-to-End Data Engineering Pipeline
<br/><br/>
We’ve now built a modern data lakehouse that brings together several powerful open-source technologies.
Our architecture uses MinIO (S3-compatible object storage) as the foundation, with Hive Metastore managing metadata and Apache Iceberg providing an advanced table format.
<br/>
Apache Spark powers large-scale data processing, while Hue offers an interactive GUI interface for Trino and Spark SQL, making SQL querying fast and intuitive.
Finally, DuckDB delivers ultra-fast local analytics directly on top of the same data.
<br/>
Now, it’s time to implement a complete end-to-end data engineering pipeline using this setup.
<br/><br/>


## 🔄 Workflow Summary
<br/><br/>

### Task 01 — Data Generation:

A source program generates customer transaction datasets every hour.
<br/><br/>
### Task 02 — Transformation & Compression:

Spark processes and compresses these files, then stores them as Iceberg tables in MinIO.
<br/><br/>
### Task 03 — Querying with Trino (via Hue):

Use Hue to run SQL queries through Trino for fast, interactive analytics.
<br/><br/>
### Task 04 — Loading Data into DuckDB:

Load and query the same processed data directly from DuckDB for lightweight local analytics.
