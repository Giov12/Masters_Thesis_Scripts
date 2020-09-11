#!/bin/python

import argparse
from Bio import SeqIO
from Bio.Alphabet import IUPAC
import os


def get_arguments():
    parser = argparse.ArgumentParser(description="Convert Fasta File to Nexus format")
    parser.add_argument("-i", "--input", help="Input Fasta file", required=True)
    parser.add_argument("-o", "--output", help="output name", required=True)

    args = parser.parse_args()
    fasta_file = args.input
    nexus_file = args.output

    return fasta_file, nexus_file


def fasta2nex(fasta_file, nexus_file):

    SeqIO.convert(
        fasta_file, "fasta", nexus_file, "nexus", alphabet=IUPAC.ambiguous_dna
    )


def main():
    fasta_file, nexus_file = get_arguments()
    fasta2nex(fasta_file, nexus_file)


if __name__ == "__main__":
    main()
