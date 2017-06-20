#!/usr/bin/env python

### Irods centralization script for CIMENT users
### It allows physical move of files using sudo and
### access to the centralized files for direct download.
### The following sudo configuration must be adapted and set up:
# Defaults        env_keep="clientUserName"
# User_Alias      IRODSUSERS = %li-users
# IRODSUSERS      ALL = (irods) NOPASSWD: /usr/bin/ireg -R smh-simsu-l20-r1 -C /cargo/[A-z0-9_/]* [A-z0-9_/]*, /usr/bin/ireg -R cigri-simsu -C /scratch_r730/cargo/[A-z0-9_/]* [A-z0-9_/]*
# IRODSUSERS      ALL = (root) NOPASSWD: /bin/chown -R irods /cargo/[A-z0-9_/]*, /bin/chown -R irods /scratch_r730/cargo/[A-z0-9_/]*

import json
import ConfigParser
import os,sys
from optparse import OptionParser
import re
import getpass
import socket
import subprocess

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
IRODS_ZONE=config.get('global','irods_zone')
IRODS_DIR=config.get('global','irods_dir')
REG_RESOURCE=config.get('global','registration_resource')
ADMIN_USER=config.get('global','admin_user')

# Options parsing
parser = OptionParser()
parser.add_option("-c", "--collection",
                  action="store", type="string", dest="collection", default="",
                  help="Full path of the collection to centralize")
parser.add_option("-y", "--yes",
                  action="store_true", dest="yes", default=False,
                  help="Answer yes to all questions")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="Be verbose")
(options, args) = parser.parse_args()

# Check arguments
if options.collection == "" :
    print "Please, give the path of the collection to centralize (-c option)"
    parser.print_help()
    print "Example:"
    print "    "+os.path.basename(__file__)+" -c /cigri/home/"+getpass.getuser()+"/my_directory"
    sys.exit(1)
options.collection=options.collection.rstrip("/")


# TODO
# - Check if collection is actually a collection
p = subprocess.Popen(['ils', options.collection], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
if err != "":
    print "Error: Could not access to "+ options.collection+" :"
    print err
    sys.exit(2)
collection=out.splitlines()[0].rstrip(":")
if collection == "":
    print "Error: could not get collection "+ options.collection+". Is it a collection?"
    sys.exit(3)
directory=IRODS_DIR+"/"+collection.lstrip(IRODS_ZONE+"/")

# Ask for confirmation
print "Your are about to centralize:"
print " - the iRods collection "+collection
print " - into the local directory "+ directory
print " - on the resource "+REG_RESOURCE+" ("+socket.getfqdn()+")"
print "WARNING: if you accept, the files into "+collection+" won't be distributed anymore." 
print "WARNING: YOUR FILES WILL BE READABLE BY ANY CIMENT USER! Please, contact a Ciment administrator if this is a problem for you!" 
if not options.yes:
    print "Are you ok with that? (y/n)",
    sure=raw_input()
    if sure != "y" and sure != "Y":
        print "Ok, moving data!.. no, it's a joke!"
        sys.exit(0)

print
print "Moving data..."
verbose_string=""
if options.verbose:
	verbose_string="-v"
ret=os.system("sudo clientUserName={} -u {} iphymv {} -r -R {} {}".format( 
    getpass.getuser(),ADMIN_USER,verbose_string,REG_RESOURCE,collection))
if ret != 0:
    print "Error while moving data. Exiting!"
    sys.exit(4)
print "Files moved."
print "Removing replicas if any (irods bug workaround)..."
ret=os.system("itrim {} -S {} -N 1 -r {}".format(verbose_string,REG_RESOURCE,collection))
print "Changing rights on the files..."
ret=os.system("sudo chmod 755 -R {}".format(IRODS_DIR+"/home/"+getpass.getuser()))
#TODO: find a way for finer rights: problem as our users don't have a group at their logname
#ret=os.system("sudo chown {} -R {}".format(getpass.getuser(),directory))
if ret != 0:
    print "Error while changing the owner of the files. Exiting!"
    sys.exit(4)
print "You can access to your files into:"
print "   "+config.get('global','external_fqdn')+":"+directory

