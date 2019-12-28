#!/usr/bin/env python3
import re
import argparse
from sys import argv
from email.parser import BytesParser, Parser
from email.policy import default


## Find and print the user agent from an email header
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_agent(filename):
    agent = "Not found"
    next = False
    with open(filename, "r") as fp:
        for line in fp:
            if(next):
                agent += line
                next = False
            if("User-Agent:" in line.split()):
                tmp = line.split("User-Agent:")
                agent = tmp[1]
                next = True
    print("User-Agent: %s" % agent)


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


## Extract and print the route an email took
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_route(filename):
    # Create an array containing all the lines containg route information
    rt = []
    count = 0
    found = False
    with open(filename, 'r') as fp:
        for line in fp:
            if(count == 2):
                found = False
                count = 0
            elif(found):
                rt.append(line)
                count += 1
            elif("Received:" in line.split()):
                rt.append(line)
                found = True

    # This array will hold route pairs (from->to) with last hop first
    order= []
    ips = []

    for i in range(len(rt)):
        seperated = rt[i].split()
        if("Received:" in seperated):
            if("by" not in rt[i+1].split()):
                order.append("NULL")
                order.append(seperated[2])
                ips.append("None")
                ips.append(extract_ip(rt[i]))
            else:
                order.append(seperated[2])
                ips.append(extract_ip(rt[i]))
        elif("by" in seperated):
            order.append(seperated[1])
            ips.append(extract_ip(rt[i]))

    print("\n\nHop #: From --> To")
    j = 1

    # Since the headers are analyzed from top to bottom, the route
    # information is in reverse order
    for i in range(len(order)-1, -1, -2):
        print("Hop {0}: {1} {2} --> {3} {4}" .format(j, order[i-1], ips[i-1], order[i], ips[i]))
        j += 1

## Print basic information about an email
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_basic(filename):
    #If the e-mail headers are in a file, uncomment these two lines:
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    #  Now the header items can be accessed as a dictionary:
    print("To: {}".format(headers["to"]))
    print("From: {}".format(headers["from"]))
    print("Subject: {}".format(headers["subject"]))
    print("Date: {}" .format(headers["Date"]))


if __name__ == '__main__':
    argp = argparse.ArgumentParser("tracemail.py",
        description="Analyze and display information from e-mail headers")
    argp.add_argument("-r", "--route", help="Display route information", action="store_true")
    argp.add_argument("-u", "--user_agent", help="Display user agent", action="store_true")
    argp.add_argument("FILE", help="Text file containing an email header to analyze")
    args = argp.parse_args()

print_basic(args.FILE)

if(args.user_agent):
    print_agent(args.FILE)

if(args.route):
    print_route(args.FILE)
