#!/bin/python

import os
import argparse
import tempfile
from Bio import SeqIO, AlignIO, Alphabet


def get_arguments():
    parser = argparse.ArgumentParser(description="Split Multilocus Nexus File")
    parser.add_argument("-i", "--input", help="Input nexus file", required=True)

    args = parser.parse_args()
    nexus_file = args.input

    return nexus_file


def split_nexus(nexus_file):

    splits = []

    with open(nexus_file, "r") as n:
        for line in n:
            line = line.strip()
            if "charset" in line:
                line = line.split(" = ")
                splits.append(line[1].replace(";", ""))

    cur_locus = 1  # current locus num

    for s in splits:

        tmp = tempfile.NamedTemporaryFile()  # create temp fasta

        output = "Locus_" + str(cur_locus) + ".nex"

        with open(tmp.name, "w") as t:
            for record in SeqIO.parse(nexus_file, "nexus"):
                start = int(s.split("-")[0])
                end = int(s.split("-")[1])
                split_seq = record.seq[start:end]
                t.write("%s\n%s\n" % ((">" + record.id), split_seq))  # write temp fasta

        with open(tmp.name, "r") as input_handle:
            AlignIO.convert(
                input_handle, "fasta", output, "nexus", alphabet=Alphabet.generic_dna
            )

        cur_locus += 1


def Make_N_Missing(nexus_file):
    for file in os.listdir():
        if file.startswith("Locus_"):  # skip input file
            with open(file, "r") as f:
                nex_data = f.read()

            nex_data = nex_data.replace(
                "missing=?", "missing=N"
            )  # replace missing character

            with open(file, "w") as f:
                f.write(nex_data)


def main():
    nexus_file = get_arguments()

    split_nexus(nexus_file)

    Make_N_Missing(nexus_file)


if __name__ == "__main__":
    main()

