# Tracemail - A simple e-mail header analyzer script

**Description**

Tracemail is a small, simply Python 3.X.X script to print information about
an e-mail. Tracemail analyzes different aspects of e-mail headers and prints
the information. This script was created to provide a simple program
for analyzing e-mail headers with as few dependencies as possible. This
program takes one or more e-mails in plain text format as input. Simply
copy the source of an email, including the headers, and paste it into
a plain text file.


**Getting Started**

Get a copy of the source code and change into the tracemail directory.

    cd tracemail

Then run the program with the -h or --help options for help.

    ./tracemail -h

An example of using tracemail to display some basic information about an
e-mail, simply supply an e-mail file with no arguments

    ./tracemail ./email.txt

To display information about the route an e-mail took, use the -r option.

    ./tracemail -r ./email.txt

Multiple e-mails can be specified at once to process multiple e-mails.

    ./tracemail ./email1.txt ./email2.txt ./email3.txt



**To Do**

- [ ] Add an option to print the location of an IP address using GeoIP
- [ ] Parse and display authentication information


**Contributing**

Pull requests, new feature suggestions, and bug reports/issues are
welcome.


**License**

This project is licensed under the 3-Clause BSD License also known as the
*"New BSD License"* or the *"Modified BSD License"*. A copy of the license
can be found in the LICENSE file. A copy can also be found at the
[Open Source Institute](https://opensource.org/licenses/BSD-3-Clause)
