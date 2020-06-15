These are a a couple of bash scripts that take unmodified results from ipyrad and STACKS to look at the amount of missing data in either the phylip or structure files.

Each file only takes 1 file as an input as shown below.

```bash
./count_fastq_reads.sh File.fastq.gz #takes gzip file, but can be modified to take uncompressed reads

./Missing_data_Ipyrad_Structure.sh ipyrad_output.str

./Missing_data_Structure.sh file.structure #deals with STACKS logo and assumes pop info column present

./Missing_data_phylip.sh file.phylip #deals with STACKS logo in file

./Missing_data_phylip_ipyrad.sh file.phy #slightly different format than STACKS output

```