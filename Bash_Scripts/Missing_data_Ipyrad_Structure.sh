#!/bin/bash
#This script works with the unmodified Structure output from Ipyard
#usage: Missing_data_Ipyrad_Structure.sh file.str

file=${1?Error: Please Provide Structure File}

#Count the # of -9's (missing data) per line
	count=$(cut -f6- $file | awk '{print gsub("-9","")}')

#Count the total # of markers
	total_count=$(cut -f6- $file | awk '{print NF}')

#Count the number of present information per line
	present=$(paste <(echo "$total_count") <(echo "$count") | awk '{print $1-$2}')

#Divide the # of missing data over total # of markers and output as #%
	percent=$(paste <(echo "$total_count") <(echo "$count") | awk ' { printf "%.2f\n", ($2/$1)*100 } ' | awk '{ print $1"%"}')

#Add sample names & merge the 4 variables into 1
	merged=$(cut -f1 $file | paste - <(echo "$total_count") <(echo "$present") <(echo "$count") <(echo "$percent"))

#Add a header and output as tsv
	echo "Sample_ID Total_Count     Sites_Present   Missing_Count   Percent_Missing" | cat - <(echo "$merged") | uniq > Missing_data_stats.tsv

#Print results to the shell
echo "Done!"
echo "=================================================================="
cat Missing_data_stats.tsv | column -t
