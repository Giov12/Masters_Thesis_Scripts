#!/bin/python

import argparse
from Bio import SeqIO
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Plot a Histogram of Read Lengths")
    parser.add_argument(
        '-i', '--input', help='Input fasta file', required=True)
    parser.add_argument(
        '-c', '--color', help='Choose the color of the histogram', default='grey')
    parser.add_argument('-t', '--hist_title', help='Add title to Histogram',
                        default='Distribution of Read Lengths', nargs='*')
    parser.add_argument(
        '-x', '--x_title', help='Add label for X-axis', default='Length (bp)', nargs='*')
    parser.add_argument(
        '-y', '--y_title', help='Add label for Y-axis', default='Frequency', nargs='*')

    args = parser.parse_args()
    file = args.input
    color = str(args.color)
    main_title = ' '.join(map(str, args.hist_title))
    # join input words into 1 string
    x_title = ' '.join(map(str, args.x_title))
    y_title = ' '.join(map(str, args.y_title))

    return file, color, main_title, x_title, y_title


def plot_read_lengths(file, color, main_title, x_title, y_title):

    sns.set_style("whitegrid")
    len_dict = defaultdict(int)

    with open(file, 'r') as f:
        for record in SeqIO.parse(f, 'fasta'):
            read_length = len(record.seq)  # get length of seq
            len_dict[read_length] += 1  # tally up counts for length

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(111)
    ax.bar(len_dict.keys(),  len_dict.values(), 10., color=color)
    ax.set_title(main_title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    return fig


def main():
    file, color, main_title, x_title, y_title = get_arguments()
    histogram = plot_read_lengths(file, color, main_title, x_title, y_title)
    plt.show()
    histogram.savefig("Histogram.png")


if __name__ == "__main__":
    main()
