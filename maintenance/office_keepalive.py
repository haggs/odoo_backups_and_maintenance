###############################################################################################
# This script ensures that the openoffice service is currently running, and starts
# it if not. It does it by checking for the processes:
#
#   /usr/lib/libreoffice/program/oosplash
#   /usr/lib/libreoffice/program/soffice.bin
#
# If either of them aren't running, it runs the command:
#
#   /etc/init.d/office
#
#   Author:     Dan Haggerty
#   Date:       19/3/2015
#
###############################################################################################
import commands
import os
import logging
import logging.handlers
from datetime import *

# Setup logging
log_path = '/var/log/odoo/office_keepalive.log'
logger   = logging.getLogger('Office Keepalive Logger')
handler  = logging.handlers.RotatingFileHandler( log_path, maxBytes=100000, backupCount=0 )
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def timestamp():
    return datetime.now().strftime("[%d/%m/%Y %H:%M:%S] ")

output = commands.getoutput( 'ps -ef | grep oosplash' )

needs_restart = False

if output.count( "/usr/lib/libreoffice/program/oosplash" ) < 1:
    needs_restart = True

output = commands.getoutput( 'ps -ef | grep soffice.bin' )

if output.count( "/usr/lib/libreoffice/program/soffice.bin" ) < 1:
    needs_restart = True

if needs_restart:
    logger.error( timestamp() + "Open Office service isn't running. Starting now." )
    os.system( 'killall soffice.bin' )
    os.system( '/etc/init.d/office'  )
else:
    logger.error( timestamp() + "Open Office service is running." )
