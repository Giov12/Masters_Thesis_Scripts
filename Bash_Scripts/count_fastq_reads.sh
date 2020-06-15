#!/bin/bash

#usuage: ./count_fastq_reads.sh fastq.gz

file=${1}

file_name=$(basename $file)

count=$(echo $(zcat $file | wc -l)/4 | bc)

echo "$file_name has $count sequences"
