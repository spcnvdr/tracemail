#!/usr/bin/env python3
##############################################################################
# Copyright 2020 spcnvdr <spcnvdrr@protonmail.com>                           #
#                                                                            #
# Redistribution and use in source and binary forms, with or without         #
# modification, are permitted provided that the following conditions         #
# are met:                                                                   #
#                                                                            #
# 1. Redistributions of source code must retain the above copyright notice,  #
# this list of conditions and the following disclaimer.                      #
#                                                                            #
# 2. Redistributions in binary form must reproduce the above copyright       #
# notice, this list of conditions and the following disclaimer in the        #
# documentation and/or other materials provided with the distribution.       #
#                                                                            #
# 3. Neither the name of the copyright holder nor the names of its           #
# contributors may be used to endorse or promote products derived from       #
# this software without specific prior written permission.                   #
#                                                                            #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS        #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT          #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR      #
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT       #
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,     #
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   #
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR     #
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF     #
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING       #
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS         #
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.               #
#                                                                            #
# This file is meant to hold the functions used to print the route delays    #
# in a nice looking ASCII art box.                                           #
#                                                                            #
##############################################################################


## Print the start of the table used to display hop delays
#
def print_heading():
    print("\n")
    print("\u250C" + "\u2500"*7 + "\u252C" + "\u2500"*20 + "\u2510")
    print("\u2502" +" Hop # " + "\u2502" +  " Delay (in seconds) " + "\u2502")
    print("\u251c" + "\u2500" * 7 + "\u253c" + "\u2500" * 20 + "\u2524")


## Print a row in the hop delay table
#  @param hop the hop number to display in the row
#  @param delay the delay time to display in the row
#
def print_row(hop, delay):
    h_format = "{0:{align}{width}}".format(hop, align="^", width=7)
    d_format = "{0:{align}{width}}".format(delay, align="^", width=20)
    print("\u2502" + h_format + "\u2502" + d_format + "\u2502")


## Print the separator between rows of data in the table
#
def print_sep():
    print("\u251c" + "\u2500" * 7 + "\u253c" + "\u2500" * 20 + "\u2524")


## Print the end the table
#
def print_end():
    print("\u2514" + "\u2500" * 7 + "\u2534" + "\u2500" * 20 + "\u2518")


## Print the total delay time centered in a nice format
#
def print_total(time):

    if(time//60 != 0):
        mins = int(time // 60)
        sec = int(time % 60)
        output = "Total: " + str(mins) + " min. " + str(sec) + " sec."
        total = "{0:{align}{width}}".format(output, align="^", width=30)
        print(total)
    else:
        output = "Total: " + str(time) + " sec."
        print("{0:{align}{width}}".format(output, align="^", width=30))