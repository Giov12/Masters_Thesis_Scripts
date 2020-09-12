#!/bin/python3

import argparse
from Bio import SeqIO


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Get Putative Orthologs from Reference Using .loci File"
    )
    parser.add_argument("-i", "--input", help="Input .loci File", required=True)
    parser.add_argument(
        "-o", "--output", help="Output Name", default="Reference_Orthologs.fasta"
    )
    parser.add_argument(
        "-r", "--reference", help="Input Reference Fasta File", default=6
    )

    args = parser.parse_args()
    loci = args.input
    output = args.output
    reference = args.reference

    return loci, output, reference


def make_coordinates(loci):

    coords = {}

    locus_num = 0  # ipyrad is 0-based

    loci_file = open(loci, "r")

    for line in open(loci, "r"):
        if line.startswith("//"):
            info = line.strip().split(":")[1:]  # get cluster info
            positions = info[1]  # get positions
            scaffold = info[0]  # scaf name
            start = int(positions.split("-")[0])
            end = int(positions.split("-")[1].replace("|", ""))
            locus = "Locus_" + str(locus_num)
            coords[locus] = [scaffold, start, end]
            locus_num += 1

    loci_file.close()

    return coords


def get_orthologs(reference, coords, output):

    ref = SeqIO.parse(reference, "fasta")

    with open(str(output), "w") as out:
        for record in ref:
            for locus, vals in coords.items():
                if record.id == vals[0]:
                    ref_seq = record.seq[vals[1] - 1 : vals[2] - 1]  # 0-based
                    seq_header = ">Reference_" + locus  # seq header
                    out.write("%s\n%s\n" % (seq_header, ref_seq.upper()))  # write out


def main():
    loci, output, reference = get_arguments()
    coords = make_coordinates(loci)
    get_orthologs(reference, coords, output)


if __name__ == "__main__":
    main()
