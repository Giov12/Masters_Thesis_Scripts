#!/bin/python

import argparse
from Bio import SeqIO
import os


def get_arguments():
    parser = argparse.ArgumentParser(description="Convert Nexus file to a Fasta file")
    parser.add_argument("-i", "--input", help="Input Nexus file", required=True)
    parser.add_argument("-o", "--output", help="output name", required=True)

    args = parser.parse_args()
    nexus_file = args.input
    fasta_file = args.output

    return nexus_file, fasta_file


def nex2fasta(nexus_file, fasta_file):

    with open(nexus_file, "r") as nexus:
        with open(str(fasta_file), "w") as fasta:
            seqs = SeqIO.parse(nexus, "nexus")
            SeqIO.write(seqs, fasta, "fasta")


def main():
    nexus_file, fasta_file = get_arguments()
    nex2fasta(nexus_file, fasta_file)


if __name__ == "__main__":
    main()
