#!/usr/bin/python env
#opening input file###
import commands
import sys
import os
import shutil
from datetime import date

'''
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
 
'''


##Variable ###
APPLICATION_HOME=os.getcwd()+'/'
RUN=APPLICATION_HOME+'run/'
OUTPUT_DIR=APPLICATION_HOME+'output/'
LOG_DIR=APPLICATION_HOME+'log/'
REGISTERED_DOMAIN='register_domain.latest'
UNREGISTERED_DOMAIN='unregister_domain.latest'
DATE=date.today().strftime('%Y%m%d')
DOMAIN_FILE=sys.argv[1]
LINE_PER_FILE=50000


def FILE_PROCESS_FAILED():
        '''It will be called if supplied file doesn't exists '''
        print 'Split Failed'

def FILE_PROCESS():
        '''Function will be called for processing '''
        if DEBUG:
                print 'Info:\tCollecting all files from %s ' % RUN
        FILE_NAME=commands.getoutput('ls -1 %s' % RUN)
        FILE_NAME_LIST=FILE_NAME.split('\n')
        FILE_NAME_COUNT=len(FILE_NAME_LIST)
        INITIAL=1
        for FILE_NAME_VAR in FILE_NAME_LIST:
                print 'Progress:\t %i/%i ' % (INITIAL,FILE_NAME_COUNT)
                INITIAL+=INITIAL
                LINE_PER_FILE=400
                if DEBUG:
                        print 'Info:\tProcessing file %s ' % FILE_NAME_VAR.rstrip()
                        print 'Info:\tNumber of Lines per %i ' % LINE_PER_FILE
                SPLIT_STATUS=commands.getstatusoutput('cd %s;split -l %i %s TtY' % (RUN,LINE_PER_FILE,FILE_NAME_VAR))
                FINAL_FILE_NAME=commands.getstatusoutput('ls -1 %sTtY*' % RUN)
                FINAL_FILE_NAME_LIST=FINAL_FILE_NAME[1].split('\n')

                for VAR in FINAL_FILE_NAME_LIST:
                        if DEBUG:
                                print 'Info:\tFiles Going for Validation %s' % VAR
                        os.chdir(APPLICATION_HOME)
                        try:
                                import twisted
                        except ImportError:
                                print '\n\nError:\tKindly Install Twisted\n\n'
                        out=commands.getstatusoutput('python gethostname.py %s %s %s %s' % (VAR,REGISTERED_DOMAIN,UNREGISTERED_DOMAIN,OUTPUT_DIR))
                        #print out
                        if out[0]==0:
                                if DEBUG:
                                        print 'Info:\tProcess Completed %s' % VAR
                        REMOVE_FILE_STATUS=commands.getstatusoutput('rm -rf %s' % (VAR))
                        if REMOVE_FILE_STATUS[0]==0:
                                if DEBUG:
                                        print 'Info:\tFile removed %s' % VAR
                if DEBUG:
                        print 'Info:\tPhase Completed %s' % FILE_NAME_VAR
                FILE_NAME_STATUS=commands.getstatusoutput('cd %s;rm -rf %s' % (RUN,FILE_NAME_VAR))
                if FILE_NAME_STATUS[0]==0:
                        if DEBUG:
                                print 'Info:\tFile removed %s' % FILE_NAME_VAR






def install_status():
        try:
                shutil.rmtree(RUN)
        except OSError:
                if DEBUG:
                        print 'Info:\t Directory doesn\'t exists'
        if not os.path.exists(RUN):
                if DEBUG:
                        print 'Info:\tFile doesn\'t exists\t:%s' % RUN
                        print 'Info:\tCreating directory\t:%s' % RUN
                os.mkdir(RUN,0755)
        if not os.path.exists(OUTPUT_DIR):
                if DEBUG:
                        print 'Info:\tFile doesn\'t exists\t:%s' % OUTPUT_DIR
                        print 'Info:\tCreating directory\t:%s' % OUTPUT_DIR
                os.mkdir(OUTPUT_DIR,0755)
        #
        if not os.path.exists(LOG_DIR):
                if DEBUG:
                        print 'Info:\tFile doesn\'t exists\t:%s' % LOG_DIR
                        print 'Info:\tCreating directory\t:%s' % LOG_DIR
                os.mkdir(LOG_DIR,0755)



def program_start():
        os.chdir(OUTPUT_DIR)
        if os.path.exists(REGISTERED_DOMAIN):
                REGISTERED_DOMAIN_NEW=REGISTERED_DOMAIN.split('.')[0]+'.'+DATE
                UNREGISTERED_DOMAIN_NEW=UNREGISTERED_DOMAIN.split('.')[0]+'.'+DATE
                os.rename(REGISTERED_DOMAIN,REGISTERED_DOMAIN_NEW)
                os.rename(UNREGISTERED_DOMAIN,UNREGISTERED_DOMAIN_NEW)
        else:
                pass

        SPLIT_STATUS=commands.getstatusoutput('cd %s;split -l %i %s%s' % (RUN,LINE_PER_FILE,APPLICATION_HOME,DOMAIN_FILE))
        if SPLIT_STATUS[0]==0:
                if DEBUG:
                        print 'Info:\tProcessing the file'
                        FILE_PROCESS()
                else:
                        FILE_PROCESS()
        else:
          FILE_PROCESS_FAILED()

		  
def info():
	'''Printing information output file name with output directory information '''
        print '\n\n\tInfo:\t Registered & Unregistered domain'
        print '\tDirectory:\t %s' % OUTPUT_DIR
        print '\tRegistered domains: %s' % REGISTERED_DOMAIN
        print '\tUnregistered domains: %s' % UNREGISTERED_DOMAIN
        print '\n'


def main():
	'''It's calling to install_status, program_start,info'''
        install_status()
        program_start()
        info()



#Setting for debug mode
try:
        if sys.argv[2] =='-debug':
                DEBUG=True
except IndexError:
        DEBUG=None

		
main()

