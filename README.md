Twisted-DNS
===========

Acync network DNS lookup with exta logging 

1 async_dns.py file is the main file which accept the command line argument so that we can run the program in debugging mode and custom supply of input file. this program is responsible for following things.
 a. Validation of file hierarchy standard for the application  like run/output/log files.
 b. Take the backup of previous registered/unregistered files in output directory.
 c. Split a long text file to multiple files to save the system from memory crunch.
 d. Progress  menu.
 e. Generate the location of output files.
 f.  Supply 4 parameter to gethostname.py for further processing.

2.  gethostname.py file is responsible to create a async connection. It opens 1000 connections with DNS  and update to registered/unregistered files.

Prerequisite -
1. python
2. twisted

python modules
1. Sys
2. os
3. datetime
4. shutil
5. commands


syntax:

$python gethostname.py <inputfile> <register domain file> <unregister domain file> <output directory>

Input file format
********************
Discrption,domainname

example-
Redhat,redhat.com


Register & unregister output file
*********************************
Discrption,domainname

example-
Redhat,redhat.com


