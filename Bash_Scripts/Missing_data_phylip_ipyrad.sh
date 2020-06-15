#!/bin/bash
#Usuage: Missing_data_phylip.sh file.phy

file=${1?Error: Please Provide Phylip File}

#Count the # of sites for each pop
	total_count=$(tail -n+2 $file | awk '{print substr($0, index($0,$2))}' | awk '{print length}')

#Count the # of N's for each pop
	count=$(tail -n+2 $file | awk '{print substr($0, index($0,$2))}' | awk '{print gsub("N","")}')

#Find the difference between total_count and count
	present=$(paste <(echo "$total_count") <(echo "$count") | awk '{print $1-$2}')

#Find the % of count/total_count and output as #%
	percent=$(paste <(echo "$total_count") <(echo "$count") | awk ' { printf "%.2f\n", ($2/$1)*100 } ' | awk '{ print $1"%"}')

#Add the pop IDs and merge the 4 variables together
	merged=$(tail -n+2 $file | awk '{print $1}' | paste - <(echo "$total_count") <(echo "$present") <(echo "$count") <(echo "$percent"))

#Add header and output results as tsv
	echo 'Population_ID     Marker_Count    Sites_Present   Number_of_Ns    Percent_of_Ns' | cat - <(echo "$merged")  > Missing_Data_Phylip.tsv

#Print results to the shell
echo 'Done!'
echo '=========================================================='
cat Missing_Data_Phylip.tsv | column -t
