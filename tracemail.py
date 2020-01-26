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
# A simple Python 3.X.X script to analyze e-mail/s saved as plain text.      #
##############################################################################
import re
import argparse
from os import path
from datetime import datetime
from email.parser import BytesParser, Parser
from email.policy import default


## Return the difference between 2 datetimes in seconds
#  @param datea datetime object o subtract from
#  @param dateb datetime object to subtract
#  @returns the difference in seconds as a float
#
def time_diff(timea, timeb):
    diff = timea - timeb
    return(diff.total_seconds())


## Extract the timestamp from a "Received" field
#  @param A string of the received field
#  @returns a datetime object of the timestamp from the Received field
#
def extract_date(recfield):
    tmp = recfield.split(";")[1].lstrip()
    tmp = tmp.split()
    timestr = " "
    timestr = timestr.join(tmp[0:6])
    return(datetime.strptime(timestr, '%a, %d %b %Y %H:%M:%S %z'))


## Get all the fields present in an email's headers
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns a list of all fields found
#
def get_fields(filename):
    fields = []
    # First find all the fields present in the email headers
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    # Add each field to a list
    for i in headers:
        fields.append(i+":")

    return(fields)


## Extract a valid IPv4 address from a string
#  @param line The string to search
#  @returns The IPv4 Address found, or an empty string
#
def extract_ip(line):
    ip = re.search("\[(.*?)\]", line)
    if(ip):
            return(ip.group(0))
    else:
        a = re.search("\((.*?)\)", line)
        if(a):
            return(a.group(0))
        else:
            return("")


## Creates a list of all the received fields present in the email's headers
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns a list of received fields
#
def get_received(filename):
    rt = []
    rec = []
    tmp = ""
    found = False

    fields = get_fields(filename)

    # Parse the file looking for Received fields
    with open(filename, "r") as fp:
        for line in fp:
            sep = line.split()
            # Found the end of the field , add to rt list
            if(len(sep) != 0 and sep[0] in fields and found):
                rt.append(tmp)
                tmp = ""
                if(sep[0] != "Received:"):
                    found = False
                else:
                    # The next field is another Received
                    tmp += line
            elif(found):
                # keep adding lines until we hit another field
                tmp += line
            elif("Received:" in line.split()):
                # Found a received field, start adding lines
                tmp += line
                found = True

    # Format each received field into a single line and add to rec list
    for i in rt:
        rec.append(" ".join(i.split()))

    return(rec)


## Extract and print the route an email took
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_route(filename):
    ips =[]
    names = []
    j = 1
    rec = get_received(filename)
    #print_delay(rec)

    for i in rec:
        sep = i.split()
        if(sep[1] == "by"):
            names.append("Null")
            ips.append("None")
            names.append(sep[2])
            ips.append("")
        else:
            f = sep.index("from")
            b = sep.index("by")
            half = i.split("by")
            quart = half[1].split("for")

            names.append(sep[f+1])
            ips.append(extract_ip(half[0]))
            names.append(sep[b+1])
            ips.append(extract_ip(quart[0]))

    print("\n\nHop #: From --> To")

    for i in range(len(names)-1, -1, -2):
        print("Hop {0}: {1} {2} --> {3} {4}" .format(j, names[i-1], ips[i-1], names[i], ips[i]))
        j += 1


## Print time delay of each hop in the route
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_delay(filename):
    j = 1
    total = 0.0
    routes = get_received(filename)
    routes.reverse()

    print("\n")
    print("Hop # |  Delay (in seconds)")
    print("___________________________")
    print("{}     |   *" .format(j))
    for i in range(0, len(routes)-1):
        timea = extract_date(routes[i+1])
        timeb = extract_date(routes[i])
        diff = time_diff(timea, timeb)
        total += diff

        print("{}     |   {}" .format(j, diff))
        j += 1
    print("Total time: {} second/s" .format(total))


## Print the email's originating IP address
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_origin(filename):
    origin = "Not found"
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    if(headers["x-originating-ip"] != None):
        origin = headers["x-originating-ip"]
    print("Originating-IP: %s" % origin)


## Print the email's message ID
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_messageid(filename):
    id = "Not found"
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    if(headers["Message-ID"] != None):
        id = headers["Message-ID"]
    print("Message-ID: %s" % id)


## Find and print the user agent from an email header
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_agent(filename):
    agent = "Not found"

    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    if(headers["User-Agent"] != None):
        agent = headers["User-Agent"]
    print("User-Agent: %s" % agent)


## Print basic information about an email
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_basic(filename):

    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    #  Access the items from the headers dictionary:
    print("To: {}".format(headers["to"]))
    print("From: {}".format(headers["from"]))
    print("Subject: {}".format(headers["subject"]))
    print("Date: {}" .format(headers["Date"]))


## Parse email and print information requested via command line arguments
#  @param filename the filename of an email (with header) saved as plaintext
#  @param all if true print all the information available
#  @param messageid if true print message id if present
#  @param origin print originating IP address if present
#  @param if true print routing information
#  @param if true print user agent if present
#  @param if true print delay in seconds between hops
#
def parse_email(filename, all, messageid, origin, route, agent, delay):

    # Make sure it is a normal file and exists
    if(not path.exists(filename)):
        print("Error: The file %s was not found!" % args.FILE)
        exit(1)
    elif(not path.isfile(filename)):
        print("Error: %s is not a file" % args.FILE)
        exit(1)

    print("\nInformation for email: %s" % filename)
    print_basic(filename)

    if(origin or all):
        print_origin(filename)

    if(agent or all):
        print_agent(filename)

    if(messageid or all):
        print_messageid(filename)

    if(route or all):
        print_route(filename)

    if(delay or all):
        print_delay(filename)


if __name__ == '__main__':
    argp = argparse.ArgumentParser("tracemail.py",
        description="Analyze and display information from e-mail headers")
    argp.add_argument("-a", "--all", help="Display everything", action="store_true")
    argp.add_argument("-d", "--delay", help="Print delay in seconds between hops", action="store_true")
    argp.add_argument("-m", "--message_id", help="Display message ID", action="store_true")
    argp.add_argument("-o", "--origin", help="Display originating IP address", action="store_true")
    argp.add_argument("-r", "--route", help="Display route information", action="store_true")
    argp.add_argument("-u", "--user_agent", help="Display user agent", action="store_true")
    argp.add_argument("FILE", help="Text file/s containing an email header to analyze", nargs="+")
    args = argp.parse_args()

    for i in args.FILE:
        parse_email(i, args.all, args.message_id, args.origin, args.route,
                    args.user_agent, args.delay)
        print("_" * 80)
