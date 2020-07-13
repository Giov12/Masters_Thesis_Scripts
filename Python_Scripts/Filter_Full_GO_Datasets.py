#!/bin/python

import argparse
import pandas as pd


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Filter GO results from Biomart in TSV Format"
    )
    parser.add_argument(
        "-i", "--input", help="Input Tsv File", required=True,
    )
    parser.add_argument(
        "-dl",
        "--dataset_list",
        help="Input Dataset Names Sorted Greatest to Least",
        required=True,
    )
    parser.add_argument(
        "-rl", "--refseq_list", help="Input list of RefSeq Accssion IDs", required=True
    )
    parser.add_argument("-o", "--output", help="Specify output name", required=True)

    args = parser.parse_args()
    full_file = args.input
    dataset_list = args.dataset_list
    refseq_accessions = args.refseq_list
    output = args.output

    return full_file, dataset_list, refseq_accessions, output


def uniq_accessions(refseq_list):

    refs_list = []  # create empty list

    with open(refseq_list, "r") as r:
        for line in r:
            line = line.strip()
            if line not in refs_list:  # if accession not in list, add
                refs_list.append(line)

    return refs_list


def make_dataset_list(dataset_list):

    datasets = []

    with open(dataset_list, "r") as ds:
        for line in ds:
            line = line.strip()  # get rid of '\n' characters
            datasets.append(line)

    return datasets


def filter_main(full_file, datasets, refs_list):

    main_data = pd.read_csv(full_file, sep="\t")

    filtered_df = pd.DataFrame(columns=main_data.columns)  # new df with same columns

    for dataset in datasets:
        for ref in refs_list:
            if ref not in list(filtered_df["refseq_peptide_predicted"]):
                dataset_rows = (
                    main_data["dataset"] == dataset
                )  # get locations of dataset
                dataset_rows = main_data[dataset_rows]  # get the rows
                rows2keep = (
                    dataset_rows["refseq_peptide_predicted"] == ref
                )  # get indices of specific RefSeq Accession
                rows2keep = dataset_rows[rows2keep]  # get the rows
                new_dfs = [filtered_df, rows2keep]
                filtered_df = pd.concat(new_dfs)

    return filtered_df


def main():
    full_file, dataset_list, refseq_accessions, output = get_arguments()
    refs_list = uniq_accessions(refseq_accessions)
    datasets = make_dataset_list(dataset_list)
    filtered_df = filter_main(full_file, datasets, refs_list)
    filtered_df.to_csv(str(output), sep="\t", index=False)


if __name__ == "__main__":
    main()
