# Tracemail - A small e-mail header analyzer

**Description**

Tracemail is a small, Python 3.X.X script to print information about
an e-mail. Tracemail analyzes the headers of an e-mail and prints
information, such as the route the e-mail took, time per hop, etc.
This script was created to provide a simple program for analyzing e-mail
headers with as few dependencies as possible. This program takes one or more
e-mails in plain text format as input. Simply copy the source of an email,
including the headers, and paste it into a plain text file to use as input
for the program.

Note that this script requires a Python module named python-dateutil. It may
be a good idea to create a virtual environment using Venv to manage
dependencies without polluting the system packages


**Getting Started**

Get a copy of the source code and change into the tracemail directory.

    git clone https://github.com/spcnvdr/tracemail.git

    cd tracemail

Then install any required packages. The goal was to use only the Python
standard library, but the python-dateutils package made life a
lot easier when parsing date strings

    pip3 install -r requirements.txt

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
- [ ] Add info about how to view e-mail headers in different mail clients


**Contributing**

Pull requests, new feature suggestions, and bug reports/issues are
welcome.


**License**

This project is licensed under the 3-Clause BSD License also known as the
*"New BSD License"* or the *"Modified BSD License"*. A copy of the license
can be found in the LICENSE file. A copy can also be found at the
[Open Source Institute](https://opensource.org/licenses/BSD-3-Clause)
