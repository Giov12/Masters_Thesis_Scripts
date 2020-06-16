# Exploratory Scripts
Scripts Made During My Master's working with RAD-Seq Data

Files were tested using results from the [ipyrad](https://ipyrad.readthedocs.io/en/latest/) and [STACKS](https://catchenlab.life.illinois.edu/stacks/) pipelines

The bash scripts take unmodified results from ipyrad and STACKS to look at the amount of missing data in either the phylip or structure files.

Each file only takes 1 file as an input as shown below.

```bash
./count_fastq_reads.sh File.fastq.gz #takes gzip file, but can be modified to take uncompressed reads

./Missing_data_Ipyrad_Structure.sh ipyrad_output.str

./Missing_data_Structure.sh file.structure #deals with STACKS logo and assumes pop info column present

./Missing_data_phylip.sh file.phylip #deals with STACKS logo in file

./Missing_data_phylip_ipyrad.sh file.phy #slightly different format than STACKS output

```
***

The python scripts are used to explore some common formats in bioinformatics.

*FastaSeqLen2Histo.py* generates a histogram of the sequence lengths from a fasta file. It can be run simply by providing it
an input file

```python
python FastaSeqLen2Histo.py -i file.fasta
```
![Histogram1](/media/gio/GIO/Other/GitHub_Images/Histogram1.png)

By default it will generate a grey bar graph. Additional parameters allow you to add some customization such as `-c` to change the *color*, `-t` for a *Histogram title*, `-x` to change the *label for the X-axis*, and `-y` to change the *label for the Y-axis*.

```python
python FastaSeqLen2Histo.py -i file.fasta -c red -t My New Title -x My Sequence Length Distribution -y My Frequency Counts
```
![Histogram1](/media/gio/GIO/Other/GitHub_Images/Histogram2.png)

The *ipyrad_loci2fasta.py* script converts the *.loci* file generated from ipyrad to a fasta file.
```python
python ipyrad_loci2.fasta.py -i ipyrad_output.loci -o ipyrad_output.fasta #specify output name
```

The *AF_Plot_Using_VCF.py* script takes a *vcf* file as an input and plots the number of alleles for each Allele Frequency in the file onto a simple line plot.
This script requires the *vcf* file to have the *AF* annotation.
```python
python AF_Plot_Using_VCF.py -i file.vcf
```
The `-c` flag can be used to specify color of the line

The *Genepop2MafGraph.py* script calculates and plots the minor allele frequency ***within*** populations. The samples are divided by population depending on a *population map*, similar to the same format used in the [STACKS Software](https://catchenlab.life.illinois.edu/stacks/manual/#popmap)

```python
python Genepop2MafGraph.py -i genepop_file.txt -p population_map.txt
```

The *Pairwise_Fst_Heatmap.py* script takes the same input files as the *Genepop2MafGraph.py* script, but produces a heatmap showing the Fst values between populations.

```python
python Pairwise_Fst_Heatmap.py -i genepop_file.txt -p population_map.txt
```
The *Plot_Fis_Vals.py* script produces a bar graph showing the average Fis value for each population. This script also accepts the same population map and genepop file as the two scripts listed above.

```python
python Plot_Fis_Vals.py -i genepop_file.txt -p population_map.txt
```

The *Missing_data_phylip.py* and *Missing_data_Structure.py* calculate the amount of missing data in these types of files. Phylip files are standardized so this only needs one input
```python
python Missing_data_phylip.py -i file.phylip
```

Since structure files can vary in the amount of metadata contained within them, the *Missing_data_Structure.py* script requires to column number where the genotype information begins using the first column flag `-fc` flag. If marker labels are present, the optional header line flag (`-hl`) can be used to specify which line number this information is located on. `-mi` is the missing integer flag that is used to specify the value used for a missing genotype.
```python
python Missing_data_Structure.py -i file.structure -mi -9 -fc 3 -hl 1
```
Both of these files have an optional `-o` flag to specify an output if the user is wanting to save the tsv file.

The *Filter_blastx_hits.py* script is a custom python script that takes blastx results in tsv format (without a header) and contains 25 columns and filters it to the *"best"* hit. This is done in a few steps.
1. Filter out blasts hits with non-RefSeq Accession IDs
2. If any blast hits for query sequences that are **completely** removed, return those blast hits
3. Remove blast hits with descriptions matching *hypothetical protein* and *uncharacterized protein*
4. Repeat Step 2
5. Return the blast hits with the lowest e-values.
   
```python
python -i blastx_hits.tsv -o filtered_blastx_hits.tsv #specify output
```

The *Filter_Accessions_by_Counts.py* script takes a space delimited *Counts* file where the first column is the number of occurences (i.e. counts) and the second column is a specific Accession ID. The script takes a tsv file where a column titled **refseq_peptide_predicted** is used to help extract the same number of rows for a particular accession ID as specified by the *counts* file.

```python
python Filter_Accesssions_by_Counts.py -i Main_Accessions_Dataframe.tsv -c Counts.txt -o Filtered_Accessions_Dataframe.tsv #specify output
```