#!/bin/python

import argparse
from Bio import SeqIO


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Get Concatenated Sequence of Mapped Regions from A Reference Sequence Using a Bed file"
    )
    parser.add_argument("-b", "--bed", help="Input Bed File", required=True)
    parser.add_argument(
        "-o", "--output", help="Output Name", default="Extracted_Concat_Seq.fasta"
    )
    parser.add_argument(
        "-r", "--reference", help="Input Reference Fasta File", default=6
    )

    args = parser.parse_args()
    bed = args.bed
    output = args.output
    reference = args.reference

    return bed, output, reference


def make_region_dictionary(bed):

    regions = {}

    with open(bed, "r") as my_bed:
        for line in my_bed:
            locus = line.strip().split("\t")[3]  # get current seq name
            c_locus = locus.split("_")[1:]  # remove sample name
            c_locus = str(c_locus[0]) + "_" + str(c_locus[1])  # make into string
            start_pos = line.strip().split("\t")[1]
            end_pos = line.strip().split("\t")[2]
            scaffold = line.strip().split("\t")[0]

            if c_locus not in regions.keys():
                regions[c_locus] = [scaffold, int(start_pos), int(end_pos)]
            else:
                if (
                    int(start_pos) < regions[c_locus][1]
                ):  # get 1st start pos for that locus
                    regions[c_locus][1] = int(start_pos)
                if (
                    int(end_pos) > regions[c_locus][2]
                ):  # get last end pos for that locus
                    regions[c_locus][2] = int(end_pos)

    return regions


def make_concat_seq(reference, regions):

    concat_seq = ""  # start concat seq

    with open(reference, "r") as ref:
        for record in SeqIO.parse(ref, "fasta"):
            for vals in regions.values():
                if record.id == vals[0]:
                    seq = record.seq[vals[1] : vals[2]]
                    concat_seq = concat_seq + seq

    return concat_seq.upper()


def main():
    bed, output, reference = get_arguments()
    regions = make_region_dictionary(bed)
    concat_seq = make_concat_seq(reference, regions)

    with open(str(output), "w") as out:
        out.write(str(concat_seq))


if __name__ == "__main__":
    main()
