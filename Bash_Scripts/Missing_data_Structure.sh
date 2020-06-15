#!/bin/bash
#Please note that this script assumes the STACKS output is unmodified
#Usage: Missing_data_Structure.sh populations.structure

file=${1?Error: Please Provide Structure File}

#Count the number of 0's per line
	count=$(tail -n+3 $file | cut -f3- | awk '{print gsub("0","")}')

#Count the number of markers 
	total_count=$(tail -n+3 $file | cut -f3- | awk '{print NF}')

#Subtract the number of 0's from the total # of markers
	present=$(paste <(echo "$total_count") <(echo "$count") | awk '{print $1-$2}')

#Divide the # of 0's over the total count and print as #%
	percent=$(paste <(echo "$total_count") <(echo "$count") | awk ' { printf "%.2f\n", ($2/$1)*100 } ' | awk '{ print $1"%"}')

#Adding sample names and merge all 4 variables
	merged=$(tail -n+3 $file | cut -f1 | paste - <(echo "$total_count") <(echo "$present") <(echo "$count") <(echo "$percent"))

#Add header to the merged variable and output as tsv
echo "Sample_ID	Total_Count	Sites_Present	Missing_Count	Percent_Missing" | cat - <(echo "$merged") | uniq > Missing_data_stats.tsv

#Print results to the shell
echo "Done"
echo "===================================================================="
cat Missing_data_stats.tsv | column -t
