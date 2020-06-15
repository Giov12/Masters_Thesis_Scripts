#!/bin/python

import argparse

def get_arguments():
	parser = argparse.ArgumentParser(description = "Convert ipyrad .loci file to a Fasta file")
	parser.add_argument('-i', '--input', help = 'Input loci file', required = True)
	parser.add_argument('-o', '--output', help = 'Specify output name', required = True)
	
	args = parser.parse_args()
	loci_file = args.input
	fasta_file = args.output
	return loci_file, fasta_file
	
def loci2fasta(loci_file, fasta_file):
	
	temp_old = open(loci_file, 'r')
	
	locus_num = 1
	with open(fasta_file, 'w') as fasta:
		for line in temp_old:
			if line.startswith('//'):
				locus_num += 1 #to keep track of loci order
			else:
				l = line.rstrip().split(' ')
				sample_id = str(l[0]) #get sample ID
				header = '>' + sample_id + '_Locus_' + str(locus_num) #make standard fasta sequence header
				seq = line.replace(sample_id, '').lstrip() #get seq by removing sample ID and leading whitespace
				fasta.write('%s\n%s' % (header, seq)) #write to output file
		
		temp_old.close()
		
def main():
	loci_file, fasta_file = get_arguments()
	loci2fasta(loci_file, fasta_file)
	
if __name__ == "__main__":
	main()
