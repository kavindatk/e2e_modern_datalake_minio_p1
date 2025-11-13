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

The data loading and table creation process is shown below.

<br/><br/>
### Task 02 — Transformation & Compression:

Spark processes and compresses these files, then stores them as Iceberg tables in MinIO.
<br/><br/>
### Task 03 — Querying with Trino (via Hue):

Use Hue to run SQL queries through Trino for fast, interactive analytics.
<br/><br/>
### Task 04 — Loading Data into DuckDB:

Load and query the same processed data directly from DuckDB for lightweight local analytics.
