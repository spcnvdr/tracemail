#!/usr/bin/env python3
import re
import argparse
from os import path
from email.parser import BytesParser, Parser
from email.policy import default


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
#
def parse_email(filename, all, messageid, origin, route, agent):

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


if __name__ == '__main__':
    argp = argparse.ArgumentParser("tracemail.py",
        description="Analyze and display information from e-mail headers")
    argp.add_argument("-a", "--all", help="Display everything", action="store_true")
    argp.add_argument("-m", "--message_id", help="Display message ID", action="store_true")
    argp.add_argument("-o", "--origin", help="Display originating IP address", action="store_true")
    argp.add_argument("-r", "--route", help="Display route information", action="store_true")
    argp.add_argument("-u", "--user_agent", help="Display user agent", action="store_true")
    argp.add_argument("FILE", help="Text file/s containing an email header to analyze", nargs="+")
    args = argp.parse_args()

    for i in args.FILE:
        parse_email(i, args.all, args.message_id, args.origin, args.route,
                    args.user_agent)
        print("_" * 80)
