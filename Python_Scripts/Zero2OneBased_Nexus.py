#!/bin/python

import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Make A 0-Index Based Nexus to a 1-Indexed Based Nexus File"
    )
    parser.add_argument("-i", "--input", help="Input nexus file", required=True)
    parser.add_argument("-o", "--output", help="Specify output name", required=True)

    args = parser.parse_args()
    nexus_file = args.input
    output = args.output

    return nexus_file, output


def convert_Zero2One_Index(nexus_file, output):

    file = open(nexus_file, "r")

    nexus_data = file.readlines()  # read in info

    file.close()

    with open(output, "w") as out:
        for line in nexus_data:
            if "charset" in line:
                charset = int(line.split(" ")[1]) + 1  # make charset counts start at 1
                region = line.split(" = ")[1]  # get the site ranges
                first_pos = (
                    int(region.split("-")[0]) + 1
                )  # increase first position by 1
                second_pos = line.split("-")[1]  # get second pos
                new_line = (
                    "charset "
                    + str(charset)
                    + " = "
                    + str(first_pos)
                    + "-"
                    + second_pos
                )
                out.write(new_line)
            else:
                out.write(line)


def main():
    nexus_file, output = get_arguments()
    convert_Zero2One_Index(nexus_file, output)


if __name__ == "__main__":
    main()
