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
        "-c", "--count_file", help="Input Counts for Accessions", required=True
    )
    parser.add_argument(
        "-o", "--output", help="Specify output name", required=True)

    args = parser.parse_args()

    file = args.input
    counts = args.count_file
    output_name = args.output

    return file, counts, output_name


def filter_by_counts(file, counts):

    main_df = pd.read_csv(file, sep="\t")

    count_dict = {}  # make empty dictionary to store count info

    count_file = open(counts)

    for line in count_file:
        l = line.strip().split(" ")  # file is space delimited
        # get the count from 1st column for the accession in 2nd column
        count_dict[l[1]] = int(l[0])

    count_file.close()

    filtered_df = pd.DataFrame()  # make an empty df

    for Accession, Count in count_dict.items():
        retrieved_df = main_df[main_df.refseq_peptide_predicted == Accession].head(
            Count
        )  # get the count number of a specific accession
        df_list = [filtered_df, retrieved_df]  # merge to list to concat
        filtered_df = pd.concat(df_list)

    return filtered_df


def write_results(filtered_df, output_name):
    filtered_df.to_csv(str(output_name), sep="\t", index=False)


def main():
    file, counts, output_name = get_arguments()
    filtered_df = filter_by_counts(file, counts)
    write_results(filtered_df, output_name)


if __name__ == "__main__":
    main()
