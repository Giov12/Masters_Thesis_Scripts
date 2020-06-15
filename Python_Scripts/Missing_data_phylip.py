#!/bin/python3

from Bio import AlignIO
import pandas as pd
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate Missing Data From A Phylip File"
    )
    parser.add_argument(
        "-i", "--input", help="Input Phylip File", required=True)
    parser.add_argument(
        "-o", "--output", help="Specify output name", required=True)

    args = parser.parse_args()

    file = args.input
    output_name = args.output

    return file, output_name


def calculate_miss_data(file):

    phylip = AlignIO.read(file, "phylip")
    missing_list = []  # list to store results

    for record in phylip:
        sample_name = record.id
        if "\t" in sample_name:  # tab separated phylip files do not parse correctly
            sample_name = record.id.split("\t")[0]
            missing_nucs = record.id.split("\t")[1]
            missing_count = (missing_nucs + record.seq).count("N")
            num_sites = len(missing_nucs + record.seq)
            sites_genotyped = num_sites - missing_count
            percent_missing = (
                str(round((missing_count / num_sites) * 100, ndigits=2)) + "%"
            )
            missing_list.append(
                {
                    "Sample": sample_name,
                    "Number of Sites": num_sites,
                    "Sites Genotyped": sites_genotyped,
                    "Missing Sites": missing_count,
                    "Percent Missing": percent_missing,
                }
            )
        else:
            missing_count = record.seq.count("N")
            num_sites = len(record.seq)
            sites_genotyped = num_sites - missing_count
            percent_missing = (
                str(round((missing_count / num_sites) * 100, ndigits=2)) + "%"
            )
            missing_list.append(
                {
                    "Sample": sample_name,
                    "Number of Sites": num_sites,
                    "Sites Genotyped": sites_genotyped,
                    "Missing Sites": missing_count,
                    "Percent Missing": percent_missing,
                }
            )

    miss_df = pd.DataFrame(missing_list)  # make to df
    return miss_df


def main():
    file, output_name = get_arguments()
    miss_df = calculate_miss_data(file)
    miss_df = miss_df[  # perserve order
        [
            "Sample",
            "Number of Sites",
            "Sites Genotyped",
            "Missing Sites",
            "Percent Missing",
        ]
    ]
    miss_df.to_csv(str(output_name), sep="\t", index=False)
    print(miss_df.to_string(index=False))


if __name__ == "__main__":
    main()
