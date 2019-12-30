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
            if(count == 5):
                found = False
                count = 0
            elif(found):
                rt.append(line)
                count += 1
            elif("Received:" in line.split()):
                rt.append(line)
                found = True

    # This array will hold route pairs (from->to) with last hop first
    for i in range(len(rt)):
        print("{}: {}" .format(i, rt[i]))
        t = rt[i].split()
        for j in range(len(t)):
            print("\t{}: {}" .format(j, t[j]))
    order= []
    ips = []
    i = 0

    while(i < len(rt)):
        sep = rt[i].split()
        if(("Received:" == sep[0]) and ("from" == sep[1]) and ("by" in sep)):
            f = sep.index("from")
            order.append(sep[f+1])
            ips.append(extract_ip(rt[i]))
            b = sep.index("by")
            order.append(sep[b+1])
            # If the recieiving domain name is at the end of the line,
            # look for its IP on the next line
            if(i+1 < len(rt)-1 and b+1 == len(sep)-1):
                ips.append(extract_ip(rt[i+1]))
            else:
                ips.append(extract_ip(sep[6]))
        elif(("Received:" in sep) and ("from" in sep)):
            order.append(sep[2])
            ips.append(extract_ip(rt[i]))
            if(i+1 < len(rt) and "by" in rt[i+1]):
                t = rt[i+1].split()
                if(t.index("by") == len(t)-1):
                    tmp = rt[i+2].split()
                    order.append(tmp[0])
                    ips.append(extract_ip(rt[i+2]))
                else:
                    order.append(t[1])
                    ips.append(extract_ip(rt[i+1]))
                i += 1
            elif(i+2 < len(rt) and "by" in rt[i+2]):
                t = rt[i+2].split()
                order.append(t[2])
                ips.append(extract_ip(rt[i+2]))
                i += 2
        elif(("Received:" == sep[0]) and ("by" == sep[1])):
            order.append("NULL")
            order.append(sep[2])
            ips.append("None")
            ips.append(extract_ip(rt[i]))


        i += 1



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
