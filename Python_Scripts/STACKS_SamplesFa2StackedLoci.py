#!/bin/python3

from Bio import SeqIO
import argparse
import tempfile


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Create Stacked Loci using Stacks Samples.fa file Using MAFFT"
    )
    parser.add_argument(
        "-i", "--input", help="Input populations.samples.fa file", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Output Name", default="CLocus_Clusters.loci"
    )

    args = parser.parse_args()
    input = args.input
    output = args.output

    return input, output


def make_snp_line(tmp):

    tmp_file = open(tmp.name)
    lines = tmp_file.readlines()  # put lines into list

    seq_len = len(lines[0].strip().split("\t")[1])
    spaces = list(" " * seq_len)  # create spaces of seq length

    pos = []  # list for SNP positions

    for i in range(len(lines)):
        if i < len(lines) - 1:  # compare up to last 2 lines
            seq1 = lines[i].strip().split("\t")[1]
            seq2 = lines[i + 1].strip().split("\t")[1]
            [pos.append(x) for x in range(len(seq1)) if seq1[x] != seq2[x]]
        else:
            seq1 = lines[i - 1].strip().split("\t")[1]
            seq2 = lines[i].strip().split("\t")[1]
            [pos.append(x) for x in range(len(seq1)) if seq1[x] != seq2[x]]

    pos = list(set(pos))  # keep unique positions

    for i in pos:
        spaces[i] = "*"  # where SNP, add '*'

    spaces = "".join(spaces)  # make to string

    name_len = 0  # start a place holder for new line for positioning snps
    for line in lines:
        new_len = len(line.strip().split("\t")[0])
        if new_len > name_len:
            name_len = new_len

    place_holder = "//" + str(" " * (name_len - 2))  # for aligning columns

    snp_pos = str(place_holder + "\t" + spaces + "\n")  # reformat in the future

    return snp_pos


def create_clusters(input, output):

    with open(input, "r") as tmp:  # get starting locus num
        for line in tmp:
            if line.startswith(">"):
                locus_num = int(line.strip().split("_")[1])
                break

    fasta = open(input, "r")
    tmp = tempfile.NamedTemporaryFile(mode="w")  # create starting cluster file

    with open(str(output), "w") as Out:
        for record in SeqIO.parse(fasta, "fasta"):
            current_locus = "CLocus_" + str(locus_num) + "_"
            if current_locus in record.description:
                line = record.description + "\t" + record.seq + "\n"
                tmp.write(str(line))  # write to temp file to find SNPs for each cluster
                Out.write(str(line))
            else:
                tmp.seek(0)  # start at beginning of tmp file
                snp_pos = make_snp_line(tmp)  # get SNP line
                Out.write(snp_pos)
                locus_num = int(
                    record.description.split("_")[1]
                )  # make new locus number
                line = (
                    record.description + "\t" + record.seq + "\n"
                )  # start process again
                tmp = tempfile.NamedTemporaryFile(mode="w")
                tmp.write(str(line))
                Out.write(str(line))

    fasta.close()


def main():
    input, output = get_arguments()
    create_clusters(input, output)


if __name__ == "__main__":
    main()
