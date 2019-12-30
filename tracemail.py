#!/usr/bin/env python3
import re
import argparse
from os import path
from email.parser import BytesParser, Parser
from email.policy import default


## Print the email's originating IP address
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_origin(filename):
    origin = "Not found"
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    if(headers["x-originating-ip"] != None):
        origin = headers["x-originating-ip"]
    print("Originating-IP: {}".format(origin))


## Print the email's message ID
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_messageid(filename):

    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    print("Message-ID: {}".format(headers["Message-ID"]))


## Find and print the user agent from an email header
#  @param filename the filename of an email (with header) saved as plaintext
#
def print_agent(filename):
    agent = "Not found"
    next = False
    with open(filename, "r") as fp:
        for line in fp:
            if(next):
                if(":" not in line):
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
    order= []
    ips = []
    i = 0

    while(i < len(rt)):
        sep = rt[i].split()
        if(("Received:" == sep[0]) and ("from" == sep[1])):
            f = sep.index("from")
            if("by" in sep):
                b = sep.index("by")
                order.append(sep[f+1])
                ips.append(extract_ip(rt[i]))
                if(i+1 < len(rt)-1 and b == len(sep)-1):
                    next = rt[i+1].split()
                    order.append(next[0])
                    ips.append(extract_ip(rt[i+1]))
                elif(b != len(sep)-1):
                    order.append(sep[b+1])
                    ips.append(extract_ip(rt[i]))
                # If the recieiving domain name is at the end of the line,
                # look for its IP on the next line
                elif(i+1 < len(rt)-1 and b+1 == len(sep)-1):
                    ips.append(extract_ip(rt[i+1]))
                else:
                    ips.append(extract_ip(sep[6]))
            else:
                order.append(sep[f+1])
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
            ips.append("None")
            order.append(sep[2])
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

    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp)

    #  Access the items from the headers dictionary:
    print("To: {}".format(headers["to"]))
    print("From: {}".format(headers["from"]))
    print("Subject: {}".format(headers["subject"]))
    print("Date: {}" .format(headers["Date"]))


if __name__ == '__main__':
    argp = argparse.ArgumentParser("tracemail.py",
        description="Analyze and display information from e-mail headers")
    argp.add_argument("-a", "--all", help="Display everything", action="store_true")
    argp.add_argument("-m", "--message_id", help="Display message ID", action="store_true")
    argp.add_argument("-o", "--origin", help="Display originating IP address", action="store_true")
    argp.add_argument("-r", "--route", help="Display route information", action="store_true")
    argp.add_argument("-u", "--user_agent", help="Display user agent", action="store_true")
    argp.add_argument("FILE", help="Text file containing an email header to analyze")
    args = argp.parse_args()

    # Make sure arg is a file and exists
    if(not path.exists(args.FILE)):
        print("Error: The file %s was not found!" % args.FILE)
        exit(1)
    elif(not path.isfile(args.FILE)):
        print("Error: %s is not a file" % args.FILE)
        exit(1)

    print_basic(args.FILE)

    if(args.origin or args.all):
        print_origin(args.FILE)

    if(args.user_agent or args.all):
        print_agent(args.FILE)

    if(args.message_id or args.all):
        print_messageid(args.FILE)

    if(args.route or args.all):
        print_route(args.FILE)
