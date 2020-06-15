#!/bin/python

import pandas as pd
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Finding percentage of missing data in Structure file"
    )
    parser.add_argument(
        "-i", "--input", help="input Structure file", required=True)
    parser.add_argument(
        "-mi", "--missing_int", help="Integar Representing Missing Data", required=True,
    )
    parser.add_argument(
        "-fc", "--first_column", help="Column where genotypes begin", required=True
    )

    parser.add_argument(
        "-hl", "--header_line", help="Header Line Number", required=False, default=None
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output Name",
        required=False,
        default="Missing_Data_Structure.tsv",
    )

    args = parser.parse_args()
    file = args.input
    missing_int = args.missing_int
    first_column = args.first_column
    header_line = args.header_line
    output_name = args.output

    return file, missing_int, first_column, header_line, output_name


def get_missing_stats(file, missing_int, first_column, header_line):

    # read in as normal file instead of dataframe for speed
    str_file = open(file, "r")
    str_list = []

    if header_line is not None:
        str_file = str_file.readlines()[int(
            header_line):]  # get data past header

    for line in str_file:
        sample_name = line.split("\t")[0]
        # get the data starting from the 1st marker column
        data = str("".join(line.strip().split("\t")[int(first_column) - 1:]))
        if "-" in str(missing_int):
            num_sites = len(data.replace("-", ""))
        else:
            num_sites = len(data)
        missing_count = data.count(str(missing_int))
        percent_missing = str(
            round((missing_count / num_sites) * 100, ndigits=2)) + "%"
        genotyped_sites = num_sites - missing_count
        str_list.append(
            {
                "Sample": sample_name,
                "Total Markers": num_sites,
                "Genotyped Sites": genotyped_sites,
                "Missing Sites": missing_count,
                "Percent Missing": percent_missing,
            }
        )

    str_df = pd.DataFrame(str_list).drop_duplicates()

    return str_df


def main():
    (
        file,
        missing_int,
        first_column,
        header_line,
        output_name,
    ) = get_arguments()  # define file
    str_df = get_missing_stats(file, missing_int, first_column, header_line)
    str_df.to_csv(str(output_name), sep="\t", index=False)
    print(str_df.to_string(index=False))


if __name__ == "__main__":
    main()
