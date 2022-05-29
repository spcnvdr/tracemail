#!/usr/bin/env python3
##############################################################################
# This file is meant to hold the functions used to print the route delays    #
# in an ASCII table.                                                         #
# Copyright 2020 spcnvdr <spcnvdrr@protonmail.com>                           #
##############################################################################


# Print the separator between rows of data in the table
#
def print_sep():
    print("-" * 30)


# Print the start of the table used to display hop delays
#
def print_heading():
    print("\n")
    print_sep()
    print("|" + " Hop # " + "|" + " Delay (in seconds) " + "|")
    print_sep()


# Print a row in the hop delay table
#  @param hop the hop number to display in the row
#  @param delay the delay time to display in the row
#
def print_row(hop, delay):
    h_format = "{0:{align}{width}}".format(hop, align="^", width=7)
    d_format = "{0:{align}{width}}".format(delay, align="^", width=20)
    print("|" + h_format + "|" + d_format + "|")


# Print the total delay time centered in a nice format
#
def print_total(time):

    if time//60 != 0:
        mins = int(time // 60)
        sec = int(time % 60)
        output = "Total: " + str(mins) + " min. " + str(sec) + " sec."
        total = "{0:{align}{width}}".format(output, align="^", width=30)
        print(total)
    else:
        output = "Total: " + str(time) + " sec."
        print("{0:{align}{width}}".format(output, align="^", width=30))
