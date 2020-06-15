import numpy as np
import pandas as pd
from collections import defaultdict
from Bio.PopGen.GenePop import EasyController as gpe
import argparse
import matplotlib.pyplot as plt


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Plot Fis values from GenePop file")
    parser.add_argument(
        "-i", "--input", help="Input Genepop file", required=True)
    parser.add_argument("-p", "--pop_map",
                        help="Input Populations Map", required=True)
    args = parser.parse_args()

    file = args.input
    pop_map = args.pop_map

    return file, pop_map


def calc_Fis(file, pop_map):

    ctrl = gpe.EasyController(file)

    ind_vals = ctrl.get_avg_fis()

    pop = open(pop_map)
    pop_dict = defaultdict(list)

    for line in pop:
        m_data = line.rstrip().split("\t")
        pop_id = m_data[1]
        ind_id = m_data[0]
        pop_dict[pop_id].append(ind_id)

    pop.close()

    # manually assign pop names
    for key in pop_dict:
        for pos, inds in enumerate(ind_vals):
            inds = list(inds)
            if inds[0] in pop_dict[key]:
                inds[0] = key
                ind_vals[pos] = inds

    # make a matrix of the results for plotting

    all_pops_df = pd.DataFrame()

    for i in ind_vals:
        pop_df = pd.DataFrame.from_dict({i[0]: i[1:]})
        pop_df.index = ("Qintra", "Qinter", "Fis")
        if len(all_pops_df) == 0:
            all_pops_df = pop_df
        else:
            all_pops_df = pd.concat([all_pops_df, pop_df], axis=1)

    return all_pops_df


def plot_Fis(fis_df):

    fis_df.to_csv("Fis_Pop_Vals.tsv", sep="\t")
    fig = fis_df.plot.bar()
    fig.set_title("Average Fis Statistics")
    fig.set_xlabel("Statistic")

    return fig


def main():
    file, pop_map = get_arguments()
    fis_df = calc_Fis(file, pop_map)
    fig = plot_Fis(fis_df)
    fig.savefig("Fis_Stats.png")
    plt.show()
    print(fis_df)
    print(
        """
         According to the manual, this analysis:

         takes the observed frequencies of identical pairs of genes as estimates (Q) of
         corresponding probabilities of identity (Q) and then simply computes diversities as 1-Q:
         gene diversity within individuals (1-Qintra), and among individuals within samples (1-Qinter),
         per locus per sample, and averaged over samples or over loci.

         Where QIntra:
         Website definition: Gene Diversity between individuals

         And QInter:
         Website definition: Gene diversity among individuals within populations
     """
    )


if __name__ == "__main__":
    main()
