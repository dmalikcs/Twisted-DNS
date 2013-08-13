#!/usr/bin/env python
import sys
import os
from twisted.internet import defer
from twisted.names import client
from twisted.internet import reactor
from twisted.python import log

'''
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

'''


REGISTER_DOMAIN=sys.argv[2]
UNREGISTER_DOMAIN=sys.argv[3]
OUTPUT_DIR=sys.argv[4]
out_file=open(OUTPUT_DIR+REGISTER_DOMAIN,'a+')
error_file=open(OUTPUT_DIR+UNREGISTER_DOMAIN,'a+')

def write_to_files(result,*args):
        LIST=args[0].split(',')
        (DOMAIN_IP_STATUS,DOMAIN_IP)=result[0]
        (DOMAIN_MX_STATUS,DOMAIN_MX_INFO)=result[1]
        if DOMAIN_IP_STATUS:
                LIST.append(DOMAIN_IP)
                if DOMAIN_MX_STATUS:
                        LIST.append("1")#1 if MX record
                else:
                        LIST.append("0")#0 if MX record doesn't exists
                        print 'No Record exists'
                FINAL_DATA=','.join(LIST)
                out_file.write(FINAL_DATA)
                out_file.write('\n')
                print FINAL_DATA
        else:
                FINAL_DATA=','.join(LIST)
                error_file.write(FINAL_DATA)
                error_file.write('\n')


def write_to_files_with_stop(result,*args):
        LIST=args[0].split(',')
        (DOMAIN_IP_STATUS,DOMAIN_IP)=result[0]
        (DOMAIN_MX_STATUS,DOMAIN_MX_INFO)=result[1]
        if DOMAIN_IP_STATUS:
                LIST.append(DOMAIN_IP)
                if DOMAIN_MX_STATUS:
                        LIST.append("1")#1 if MX record
                else:
                        LIST.append("0")#0 if MX record doesn't exists
                        print 'No Record exists'
                FINAL_DATA=','.join(LIST)
                out_file.write(FINAL_DATA)
                out_file.write('\n')
                print FINAL_DATA
        else:
                FINAL_DATA=','.join(LIST)
                error_file.write(FINAL_DATA)
                error_file.write('\n')
        reactor.stop()



FH=open(sys.argv[1],'r')
FH_ARRY=FH.readlines()
VAR=len(FH_ARRY)
j=1
DIC={}
for i in FH_ARRY:
        PROCESS_DOMAIN=i.split(',')
        d = client.getHostByName(PROCESS_DOMAIN[1].rstrip('\n'))
        p = client.lookupMailExchange(PROCESS_DOMAIN[1].rstrip('\n'))
        if VAR!=j:
           j=j+1
           callbackArgs=i.rstrip('\n')
           errbackArgs=i.rstrip('\n')
           dl = defer.DeferredList([d, p], consumeErrors=True)
           dl.addCallback(write_to_files,callbackArgs)
        else:
           print 'calling last doamin'
           callbackArgs=i.rstrip('\n')
           errbackArgs=i.rstrip('\n')
           dl = defer.DeferredList([d, p], consumeErrors=True)
           dl.addCallback(write_to_files_with_stop,callbackArgs)
print 'reactor started'
reactor.run()
