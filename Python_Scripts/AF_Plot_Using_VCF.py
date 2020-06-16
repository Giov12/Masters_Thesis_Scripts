#!/bin/python3

import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from allel import read_vcf


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Plot minor allele frequency counts from a VCF file"
    )
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    parser.add_argument("-s", "--save", help="True or False", default=False)
    parser.add_argument(
        "-c", "--color", help="Line Color for Plot", default="blue")
    args = parser.parse_args()

    file = args.input
    save_results = args.save
    color = args.color

    return file, save_results, color


def count_afs(file):
    vcf_array = read_vcf(file, fields=["AF"], types={"AF": "float32"})[
        "variants/AF"
    ]  # extract only the array of AF values

    vcf_array = np.array(vcf_array)  # convert to np array

    if True in np.isnan(vcf_array):
        vcf_array = vcf_array[~np.isnan(vcf_array)]  # drop nan values
        print("Allele Frequency Counts for Nan Values Were Dropped")

    AF_vals, AF_counts = np.unique(vcf_array, return_counts=True)

    AF_dict = dict(zip(AF_vals, AF_counts))

    AF_df = pd.DataFrame(AF_dict.items())
    AF_df.columns = ["AF", "AF Counts"]  # add column names

    return AF_df


def plot_af(AF_df, color):

    fig = AF_df.plot(
        kind="line",
        figsize=(16, 10),
        x="AF",
        y="AF Counts",
        xticks=round(AF_df["AF"], ndigits=2),
        color=color,
    )
    fig.set_xlabel("Allele Frequency")
    fig.set_ylabel("Allele Counts")
    fig.set_title("Allele Frequency Counts")
    plt.xticks(rotation=45)

    return fig


def main():
    file, save_results, color = get_arguments()
    AF_df = count_afs(file)
    fig = plot_af(AF_df, color)
    if save_results == True:
        plt.savefig("AF_Counts.png")
        AF_df.to_csv("AF_Counts.tsv", sep="\t", index=False)
        plt.show()
    else:
        plt.show()


if __name__ == "__main__":
    main()
