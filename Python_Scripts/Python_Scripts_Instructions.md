These are a couple of python scripts that can be used to explore some common formats in bioinformatics.

*FastaSeqLen2Histo.py* generates a histogram of the sequence lengths from a fasta file. It can be run simply by providing it
an input file

```python
python FastaSeqLen2Histo.py -i file.fasta
```

By default it will generate a grey bar graph. Additional parameters allow you to add some customization such as `-c` to change the *color*, `-t` for a *Histogram title*, `-x` to change the *label for the X-axis*, and `-y` to change the *label for the Y-axis*.

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

The *Genepop2MafGraph.py* script calculates and plots the minor allele frequency **within** populations. The samples are divided by population depending on a *population map*, similar to the same format used in the [STACKS Software](https://catchenlab.life.illinois.edu/stacks/manual/#popmap)

```python
python Genepop2MafGraph.py -i genepop_file.txt -p population_map.txt
```

The *Pairwise_Fst_Heatmap.py* script takes the same input files as the *Genepop2MafGraph.py* script, but produces a heatmap showing the Fst values between populations.

```python
python Pairwise_Fst_Heatmap.py -i genepop_file.txt -p population_map.txt
```