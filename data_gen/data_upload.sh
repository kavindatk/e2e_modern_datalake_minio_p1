#!/bin/bash

# Get the most recent file details

# Call the inotify_monitor.sh and capture the output
file_path=$(/data/data_gen/./inotify_monitor.sh)

# Extract filename from the path
filename=$(basename "$file_path")

# Extract date and hour from the filename
dateval=${filename:0:8}
hourval=${filename:9:2}

# Print the variables
echo "file_path = $file_path"
echo "dateval = $dateval"
echo "hourval = $hourval"

# Uplaod file to MINIO S3 bucket
mc cp $file_path myminio/cusdatabucket/customer_data/dateval=$dateval/hourval=$hourval/


# Delete uploaded file

rm -rf $file_path
