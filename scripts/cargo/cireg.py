#!/usr/bin/env python

### Irods registration script for CIMENT users
### It allows registration of files using sudo.
### The following sudo configuration must be adapted and set up:
# Defaults        env_keep="clientUserName"
# User_Alias      IRODSUSERS = %li-users
# IRODSUSERS      ALL = (irods) NOPASSWD: /usr/bin/ireg -R smh-simsu-l20-r1 -C /cargo/[A-z0-9_/]* [A-z0-9_/]*, /usr/bin/ireg -R cigri-simsu -C /scratch_r730/cargo/[A-z0-9_/]* [A-z0-9_/]*
# IRODSUSERS      ALL = (root) NOPASSWD: /bin/chown -R irods /cargo/[A-z0-9_/]*, /bin/chown -R irods /scratch_r730/cargo/[A-z0-9_/]*
### This script also relies on "at", so check that it is installed
### Finally, the following iRods rule must be adapted and set up into the core.re file of the "cargo" resource:
# acPostProcForFilePathReg {delay("<PLUSET>1s</PLUSET>") {msiSysReplDataObj("cigri-simsu","null");}}

import json
import ConfigParser
import os,sys
from optparse import OptionParser
import re
import getpass
import socket

# Configuration file opening
config=ConfigParser.ConfigParser()
DEFAULT_CONFIG_FILE="/usr/local/etc/cireg.conf"
try:
    if not os.path.isfile(os.environ['CIREG_CONF_FILE']):
        raise
except:
    if os.path.isfile(DEFAULT_CONFIG_FILE):
        config.read(DEFAULT_CONFIG_FILE)
    else:
        sys.stderr.write("Error: could not load configuration file!\n")
        sys.stderr.write("The configuration file is searched into "+DEFAULT_CONFIG_FILE+" or in the location given by the $CHANDLER_CONF_FILE environement variable\n")
        sys.exit(1)
else: 
    config.read(os.environ['CIREG_CONF_FILE'])


# Get some variables from the configuration file
CARGO_DIR=config.get('global','cargo_dirs').split(",")
IRODS_ZONE=config.get('global','irods_zone')
REG_RESOURCE=config.get('global','registration_resource')
DIST_RESOURCE=config.get('global','distribution_resource')
ADMIN_USER=config.get('global','admin_user')

# Options parsing
parser = OptionParser()
parser.add_option("-c", "--collection",
                  action="store", type="string", dest="collection", default="",
                  help="Full path of the directory to register as an irods collection")
parser.add_option("-y", "--yes",
                  action="store_true", dest="yes", default=False,
                  help="Answer yes to all questions")
parser.add_option("-K", "--checksum",
                  action="store_true", dest="checksum", default=False,
                  help="Calculate a checksum on the iRODS server and store with the file details")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Be verbose")
(options, args) = parser.parse_args()

# Check arguments
if options.collection == "" :
    print "Please, give the path of the directory to register (-c option)"
    parser.print_help()
    print "Example:"
    print "    "+os.path.basename(__file__)+" -c "+CARGO_DIR[0]+"/my_directory"
    sys.exit(1)
options.collection=options.collection.rstrip("/")

# Check permissions
dir_ok=0
for cargo in CARGO_DIR:
    if re.match("^"+cargo,options.collection):
        dir_ok=1
if dir_ok == 0:
    print "Directory "+options.collection+" not allowed!"
    print "The directory should be inside one of those repositories: "+", ".join(CARGO_DIR)
    sys.exit(2)
if not os.access(options.collection, os.W_OK):
    print "Permission denied!"
    print options.collection+": directory not found or no write access" 
    sys.exit(2)

irods_collection="/"+IRODS_ZONE+"/home/"+getpass.getuser()+"/"+os.path.basename(options.collection)

# Ask for confirmation
print "Your are about to register:"
print " - the Unix directory "+options.collection
print " - of the resource "+REG_RESOURCE+" ("+socket.getfqdn()+")"
print " - into the iRods collection "+irods_collection
print "Data will be distributed on "+DIST_RESOURCE+" in the background."
print "WARNING: if you accept, the files into "+options.collection+" won't be accessible directly anymore." 
if not options.yes:
    print "Are you ok with that? (y/n)",
    sure=raw_input()
    if sure != "y" and sure != "Y":
        print "Ok, registering!.. no, it's a joke!"
        sys.exit(0)

print
print "Registering..."
verbose_string=""
if options.verbose:
	verbose_string="-v"
checksum_string=""
if options.checksum:
	checksum_string="-K"
cmd="sudo clientUserName={} -u {} ireg {} {} -R {} -C {} {}".format(
    getpass.getuser(),ADMIN_USER,verbose_string,checksum_string,REG_RESOURCE,options.collection,irods_collection)
print cmd
ret=os.system(cmd)
if ret != 0:
    print "Error while registering. Exiting!"
    sys.exit(4)
print "Files registered."
print "Changing the owner of data to "+ADMIN_USER+" ..."
ret=os.system("sudo chown -R {} {}".format(ADMIN_USER,options.collection))
if ret != 0:
    print "Error while changing the owner of the files. Exiting!"
    sys.exit(4)
print "Programming cleaning..."
ret=os.system("echo itrim -S {} -r -N 1 {}|at now + 12 hours".format(REG_RESOURCE,irods_collection))
print "Distribution will run in the background, but files are already accessible from every irods connected node."
print "Cleaning of the current cargo resource is programmed in 12 hours"

