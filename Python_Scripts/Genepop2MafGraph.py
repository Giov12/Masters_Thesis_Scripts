#!/bin/python

import numpy as np
import pandas as pd
from collections import defaultdict, OrderedDict
from Bio.PopGen.GenePop import Controller as gpc
import argparse
import matplotlib.pyplot as plt


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Plot minor allele frequencies from GenePop file"
    )
    parser.add_argument(
        "-i", "--input", help="Input Genepop file", required=True)
    parser.add_argument("-p", "--pop_map",
                        help="Input Populations Map", required=True)
    args = parser.parse_args()

    file = args.input
    pop_map = args.pop_map

    return file, pop_map


def pop_map_format(pop_map):
    temp = open(pop_map)
    temp_dict = defaultdict(list)
    pop_dict = defaultdict(list)
    for line in temp:
        m_data = line.rstrip().split("\t")
        pop_id = m_data[1]
        ind_id = m_data[0]
        temp_dict[pop_id].append(ind_id)

    for key in temp_dict:
        if key is not int:  # change popID's to integers
            for pos, key in enumerate(temp_dict.keys()):
                for i in range(len(temp_dict)):
                    if pos == i:
                        for v in temp_dict[key]:
                            pop_dict[i + 1].append(v)
        else:
            pop_dict = temp_dict

    temp.close()

    return OrderedDict(pop_dict), list(temp_dict.keys())


def calc_maf(file, pop_dict, pop_names):

    ctrl = gpc.GenePopController()

    num_of_pop = len(pop_dict)
    mafs = []
    bins = 20

    pop_iter, loci_iter = ctrl.calc_allele_genotype_freqs(file)
    del(pop_iter)  # unused output

    for i in range(num_of_pop):
        mafs.append([0] * bins)  # bins of 0s

    for locus_info in loci_iter:
        pop_loci = locus_info[2]  # get ind_id, allele_freq, allele_cnt
        for popID, indID in pop_dict.items():
            for i in pop_loci:
                if i[0] in indID:  # if ind_id matches indID from dictionary
                    reform_data = map(
                        lambda x: 0 if x == "-" else x, i[1]
                    )  # change missing to 0
                    new_pop_loci = [
                        popID,
                        reform_data,
                    ]  # make a list with popID instead of indID
                    maf = min(new_pop_loci[1])  # get min allele freq
                    if maf == 0:  # don't count 0's
                        continue
                    else:
                        # current bin
                        cbin = min([bins - 1, int(maf * 2 * bins)])
                        mafs[int(popID) - 1][cbin] += 1

    mafs_df = pd.DataFrame(mafs)
    mafs_df.columns = ["%.3f" % (x / float(bins * 2))
                       for x in range(bins + 1)][1:]
    mafs_df.index = pop_names  # get original pop names
    mafs_df.sort_index(inplace=True)
    mafs_df.insert(0, 0.000, 0)  # add 0's for frequency of 0
    mafs_df.to_csv("Maf.tsv", sep="\t")
    mafs_df2 = mafs_df.T  # transpose x with y for plotting

    return mafs_df2


def plot_maf(mafs_df):

    fig = mafs_df.plot(kind="line", figsize=(16, 10))
    fig.set_xlabel("MAF")
    fig.set_ylabel("Allele Counts")
    fig.set_title("MAF in bins of 0.025")
    fig.xaxis.set_ticks(np.arange(0, 21, 1))
    fig.xaxis.set_ticklabels(np.round(list(np.arange(0, 0.525, 0.025)), 3))

    return fig


def main():
    file, pop_map = get_arguments()
    pop_dict, pop_names = pop_map_format(pop_map)
    mafs_df = calc_maf(file, pop_dict, pop_names)

    fig = plot_maf(mafs_df)
    fig.savefig("Maf_Plot.png")
    plt.show()


if __name__ == "__main__":
    main()
