#!/bin/python

import pandas as pd
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Filter blastx hits to RefSeq Accessions Only and Non-Predicted Protein Descriptions"
    )
    parser.add_argument(
        "-i", "--input", help="Input blastx tsv file", required=True)
    parser.add_argument(
        "-o", "--output", help="Specify output name", required=True)
    args = parser.parse_args()

    file = args.input
    output_name = args.output

    return file, output_name


def filter_blast_hits(file):

    blast_hits = pd.read_csv(file, sep="\t", header=None)

    # add column values to blast.tsv results
    blast_columns = [
        "qseqid",
        "sseqid",
        "pident",
        "length",
        "mismatch",
        "gapopen",
        "qstart",
        "qend",
        "sstart",
        "send",
        "evalue",
        "bitscore",
        "sallseqid",
        "score",
        "nident",
        "positive",
        "gaps",
        "ppops",
        "qframe",
        "sframe",
        "qseq",
        "sseq",
        "qlen",
        "slen",
        "salltitles",
    ]

    blast_hits.columns = blast_columns  # make column names
    filtered_blast_hits = blast_hits[
        blast_hits["sseqid"].str.startswith("XP_")
    ]  # keeps rows with only RefSeq Accession IDs

    for (
        i
    ) in (
        blast_hits.qseqid.values
    ):  # return any query sequence hits that were completely removed
        if i not in filtered_blast_hits.qseqid.values:
            removed_hits = blast_hits[blast_hits.qseqid == i]
            dfs = [filtered_blast_hits, removed_hits]
            filtered_blast_hits = pd.concat(dfs)

    unwanted_list = [
        "hypothetical protein",
        "uncharacterized protein",
    ]  # list of descriptions to filter out

    filtered_blast_hits = filtered_blast_hits[  # remove rows with unwanted descriptions
        ~filtered_blast_hits.salltitles.str.contains("|".join(unwanted_list))
    ]

    for (
        i
    ) in (
        blast_hits.qseqid.values
    ):  # return completely removed query sequence hits again
        if i not in filtered_blast_hits.qseqid.values:
            removed_hits = blast_hits[blast_hits.qseqid == i]
            dfs = [filtered_blast_hits, removed_hits]
            filtered_blast_hits = pd.concat(dfs)

    sorted_filtered_blast_hits = filtered_blast_hits.sort_values(
        by=["qseqid", "evalue"], ascending=[True, True]
    )  # Sort by qseqid and lowest-greatest evalue

    filtered_blast_hits = sorted_filtered_blast_hits.drop_duplicates(
        subset="qseqid", keep="first"
    )  # remove duplicates and keep blast hit with the lowest e-value

    return filtered_blast_hits


def write_results(filtered_blast_hits, output_name):
    hits_kept = len(filtered_blast_hits)
    print("A total of %d hits were kept" % hits_kept)
    filtered_blast_hits.to_csv(str(output_name), sep="\t", index=False)


def main():
    file, output_name = get_arguments()
    filtered_blast_hits = filter_blast_hits(file)
    write_results(filtered_blast_hits, output_name)


if __name__ == "__main__":
    main()
