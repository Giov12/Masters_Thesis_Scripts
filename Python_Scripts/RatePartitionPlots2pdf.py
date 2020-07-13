#!/bin/python

import pandas as pd
import argparse
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pltpdf
import warnings


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Create a PDF with Line Plots of a Paritioned Rate File from IQTREE"
    )
    parser.add_argument("-i", "--input", help="Input Parition Rate File", required=True)
    parser.add_argument(
        "-o", "--output", help="Output PDF Name", default="Plotted_Rates.pdf"
    )
    parser.add_argument("-c", "--color", help="Line Color for Plot", default="red")
    args = parser.parse_args()

    file = args.input
    output = args.output
    color = args.color

    return file, output, color


def create_rate_dict(file):

    current_partition = pd.DataFrame(columns=["Rate"])

    pattern = "SITE RATES FOR PARTITION"

    rates_dict = {}

    with open(file, "r") as rates:
        for line in rates:
            if pattern in line:
                if len(current_partition) > 0:
                    rates_dict[partition_name] = round(  # get average rate
                        current_partition["Rate"].mean(), ndigits=5
                    )
                    current_partition = pd.DataFrame(columns=["Rate"])
                    partition_name = line.strip().replace(":", "")
                else:
                    partition_name = line.strip().replace(":", "")
            elif "Category" in line:
                continue
            else:
                rate = float(line.strip().split("\t")[1])
                row2insert = {"Rate": rate}
                current_partition = current_partition.append(
                    row2insert, ignore_index=True
                )
    rates_dict[partition_name] = round(
        current_partition["Rate"].mean(), ndigits=5
    )  # add last parition

    return rates_dict


def plot_partition(partition, color, title, rates_dict):

    fig = partition.plot(kind="line", figsize=(16, 12), x="Site", y="Rate", color=color)
    fig = plt.gcf()
    plt.xlabel("Site Position", fontsize=15)
    plt.ylabel("Rate", fontsize=15)
    plt.title(title, fontsize=15)
    avg_rate = "Avg Rate: " + str(rates_dict[title])
    ax = plt.axes()
    plt.text(
        0.97,
        0.94,
        avg_rate,
        horizontalalignment="right",
        verticalalignment="top",
        fontsize=15,
        transform=ax.transAxes,
    )

    return fig


def generate_pdf(output, file, color, rates_dict):

    pattern = "SITE RATES FOR PARTITION"

    all_partitions = pd.DataFrame(columns=["Site", "Rate"])

    current_partition = pd.DataFrame(columns=["Site", "Rate"])

    pos = 1

    with pltpdf.PdfPages(str(output)) as pdf:
        with open(file, "r") as rates:
            for line in rates:
                if pattern in line:
                    if len(current_partition) > 0:  # if parition info collected
                        fig = plot_partition(
                            current_partition, color, plt_title, rates_dict
                        )
                        pdf.savefig(fig)
                        current_partition = pd.DataFrame(
                            columns=["Site", "Rate"]
                        )  # start new parition df
                        plt_title = line.strip().replace(":", "")
                    else:
                        plt_title = line.strip().replace(":", "")
                elif "Category" in line:  # skip columns' names row
                    continue
                else:
                    site = int(line.strip().split("\t")[0])
                    rate = float(line.strip().split("\t")[1])
                    row2insert = pd.DataFrame({"Site": site, "Rate": rate}, index=[0])
                    current_partition = current_partition.append(
                        row2insert, ignore_index=True
                    )

                    mainrow = pd.DataFrame({"Site": pos, "Rate": rate}, index=[0])
                    all_partitions = all_partitions.append(mainrow, ignore_index=True)
                    pos += 1

        fig = plot_partition(current_partition, color, plt_title, rates_dict)
        pdf.savefig(fig)  # save last fig

        # now to save a plot for all the merged paritions
        fig = all_partitions.plot(
            kind="line", figsize=(16, 12), x="Site", y="Rate", color=color
        )
        fig = plt.gcf()
        plt.xlabel("Site Position")
        plt.ylabel("Rate")
        plt.title("All Partitions")
        avg_rate = "Avg Rate: " + str(round(all_partitions["Rate"].mean(), ndigits=5))
        ax = plt.axes()
        plt.text(
            0.97,
            0.94,
            avg_rate,
            horizontalalignment="right",
            verticalalignment="top",
            fontsize=15,
            transform=ax.transAxes,
        )
        pdf.savefig(fig)


def main():

    warnings.filterwarnings(
        "ignore", category=UserWarning
    )  # suppress plotting warnings
    plt.rcParams.update({"figure.max_open_warning": 0})

    file, output, color = get_arguments()
    rates_dict = create_rate_dict(file)

    generate_pdf(output, file, color, rates_dict)


if __name__ == "__main__":
    main()
