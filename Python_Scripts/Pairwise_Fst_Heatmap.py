#!/bin/python

import numpy as np
import seaborn as sns
import pandas as pd
from Bio.PopGen.GenePop import Controller as gpc
import argparse
import matplotlib.pyplot as plt


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Create Multilocus Pairwise Fst Heatmap"
    )
    parser.add_argument(
        "-i", "--input", help="Input Genepop file", required=True)
    parser.add_argument("-p", "--pop_map",
                        help="Input Populations Map", required=True)
    args = parser.parse_args()

    file = args.input
    pop_map = args.pop_map

    return file, pop_map


def calc_pairwise_fst(file):

    ctrl = gpc.GenePopController()
    print("Calculating Average Fst values")
    fpair_iter, avg = ctrl.calc_fst_pair(file)
    del(fpair_iter)  # remove unused output

    return avg


def plot_heatmap(avg, pop_map):

    pops = []

    pop_file = open(pop_map, "r")

    for line in pop_file:
        l = line.rstrip().split("\t")
        pop = l[1]
        if pop not in pops:
            pops.append(pop)

    pop_file.close

    num_pops = len(pops)

    pop_key = {}
    for pos, pop in enumerate(pops):
        pop_key[pos] = pop

    min_pair = min(avg.values())
    max_pair = max(avg.values())

    arr = np.ones((num_pops - 1, num_pops - 1, 3), dtype=float)

    print("Plotting")
    sns.set_style("white")
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)

    for row in range(num_pops - 1):
        for col in range(row + 1, num_pops):
            val = avg[(col, row)]
            norm_val = (val - min_pair) / (
                max_pair - min_pair
            )  # to help scale the color
            ax.text(col - 1, row, "%.3f" % val, ha="center")
            if norm_val == 0.0:
                arr[row, col - 1, 0] = 1
                arr[row, col - 1, 1] = 1
                arr[row, col - 1, 2] = 0
            elif norm_val == 1.0:
                arr[row, col - 1, 0] = 1
                arr[row, col - 1, 1] = 0
                arr[row, col - 1, 2] = 1
            else:
                arr[row, col - 1, 0] = 1 - norm_val
                arr[row, col - 1, 1] = 1
                arr[row, col - 1, 2] = 1

    ax.imshow(arr, interpolation="none")
    ax.set_xticks(range(num_pops - 1))
    ax.set_xticklabels(pops[1:])
    ax.set_yticks(range(num_pops - 1))
    ax.set_yticklabels(pops[:-1])
    ax.set_title("Average Multilocus Fst")

    return fig, pop_key


def write_to_tsv(avg, pop_key):

    pop_dict = {}

    for key, val in avg.items():
        new_key = list(key)
        temp = [pop_key.get(item, item) for item in new_key]
        pair = temp[0] + "_" + temp[1]
        pop_dict[pair] = val

        pop_df = pd.DataFrame.from_dict(pop_dict, orient="index")
        pop_df.to_csv("Pairwise_Fst_vals.tsv", sep="\t", header=False)


def main():
    file, pop_map = get_arguments()
    avg = calc_pairwise_fst(file)
    fig, pop_key = plot_heatmap(avg, pop_map)
    write_to_tsv(avg, pop_key)
    plt.savefig("Average_Multilocus_Fst_Plot.png")
    plt.show()


if __name__ == "__main__":
    main()
