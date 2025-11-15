#!/bin/bash

# Description: Executes a Spark job inside the spark_master container and logs output.
# Author: Kavinda Thennakoon

# Environment setup for cron
PATH=/usr/local/bin:/usr/bin:/bin

# Variables
CONTAINER_NAME="spark_master"
SPARK_SUBMIT="/opt/spark/bin/spark-submit"
MASTER_URL="spark://node01:7077"
SPARK_JOB="/opt/spark/codes/spark_data_comp_trans.py"

# Spark configurations
POOL="high"
EXECUTOR_CORES=2
EXECUTOR_MEMORY="4g"
DRIVER_MEMORY="4g"
MAX_CORES=6

# Logging
LOG_DIR="/home/hadoop/JOBS/log/spark_jobs"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/spark_job_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Execute Spark job inside Docker and log output
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Spark job..." >> $LOG_FILE
docker exec  $CONTAINER_NAME $SPARK_SUBMIT \
  --master $MASTER_URL \
  --conf spark.scheduler.pool=$POOL \
  --conf spark.executor.cores=$EXECUTOR_CORES \
  --conf spark.executor.memory=$EXECUTOR_MEMORY \
  --conf spark.driver.memory=$DRIVER_MEMORY \
  --conf spark.cores.max=$MAX_CORES \
  $SPARK_JOB >> $LOG_FILE 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Spark job completed." >> $LOG_FILE
