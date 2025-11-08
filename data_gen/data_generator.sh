#!/bin/bash

# Set output file path
destination_file="/data/data_gen/file/"

# Execute Python file
python /data/data_gen/data_generator.py

# File copy path
source_path="/data/data_gen/staging/*.log"

mv $source_path $destination_file


