#*****************************************************************************************************
#*****************************************************************************************************
#   Author : Kavinda Thennakoon
#   Date : 2025-11-14
#   Period : Every Hour
#   Program : Customer Data Compression and Traformation and save into Iceberg tables
#*****************************************************************************************************
#*****************************************************************************************************


import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import StringType , ArrayType , IntegerType
from datetime import datetime, timedelta

def data_transformation(path):
    df = spark.read.csv(path + "*.log", header=True, inferSchema=True)
    
    
    # Do some small transformations (Dummy transformations for example)
    
    df = df.withColumn("transction_date", f.to_date(f.col("date"), "yyyyMMdd"))
    df = df.withColumn("purchase_units", (f.floor(f.rand() * 100) + 1).cast("int"))
    df = df.withColumn("discount_percentage", (f.floor(f.rand() * 25) + 1).cast("decimal(5,2)"))
    df = df.withColumn("transction_amount", (f.col("random_number")/100).cast("decimal(10,2)"))
    df = df.withColumn("dateval", f.lit(dateval))
    
    # Drop unwanted columns
    df = df.drop("date","time","random_number")
    
    #df.printSchema()
    
    #df.show(truncate=False)    
    
    return df

def data_saving_iceberg(df):
    print("Saving data into Iceberg table")
    
    spark.sql("CREATE DATABASE IF NOT EXISTS iceberg_catalog.my_db")
    
    df.writeTo("iceberg_catalog.my_db.customer_data") \
        .using("iceberg") \
        .tableProperty("write.format.default", "parquet") \
        .tableProperty("write.parquet.compression-codec", "snappy") \
        .partitionedBy("dateval") \
        .append()
    

def main():
    # Stage 01 - Get User base and save
    print("Date:", date_str)
    print("Time:", time_str)
    
    minio_path = "s3a://cusdatabucket/customer_data/dateval={}/hourval={}/".format(date_str, time_str)
    
    print("MINIO Path:", minio_path)
    
    df_trans = data_transformation(minio_path)
    
    data_saving_iceberg(df_trans)
             
    spark.stop()
    

if __name__ == "__main__" :

    # Current datetime
    now = datetime.now()


    # Subtract 2 hours
    two_hours_before = now - timedelta(hours=2)

    # Format date as yyyy-MM-dd
    date_str = two_hours_before.strftime("%Y%m%d")
    dateval = two_hours_before.strftime("%Y-%m-%d")

    # Format time as HH:MM:ss
    time_str = two_hours_before.strftime("%H")
    
    app_name = "customer_data_saving_{}_{}".format(dateval, time_str)
    spark = SparkSession.builder.master("spark://node01:7077").appName(app_name).enableHiveSupport().getOrCreate()
 
    main()
    

