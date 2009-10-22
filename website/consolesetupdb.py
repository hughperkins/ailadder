#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#  more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in the file licence.txt; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
# 1307 USA
# You can find the licence also on the web at:
# http://www.opensource.org/licenses/gpl-license.php
#

import sys
import os
from optparse import OptionParser

from core import sqlalchemysetup

import config

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

def create():
   print "creating all..."
   sqlalchemysetup.createalltables()

def drop():
   print "dropping all..."
   sqlalchemysetup.dropalltables()

def usage():
   print sys.argv[0] + " [create|drop|reload]"

def main():
   if len(sys.argv) < 2:
      usage()
      return

   action = sys.argv[1]
   if action == 'create':
      sqlalchemysetup.setupwithcredentials( config.dbengine, config.dbuser, config.dbpassword, config.dbhost, config.dbname )
      create()
      sqlalchemysetup.close()
   elif action == 'drop':
      sqlalchemysetup.setupwithcredentials( config.dbengine, config.dbuser, config.dbpassword, config.dbhost, config.dbname )
      drop()
      sqlalchemysetup.close()
   elif action == 'reload':
      sqlalchemysetup.setupwithcredentials( config.dbengine, config.dbuser, config.dbpassword, config.dbhost, config.dbname )
      drop()
      create()
      sqlalchemysetup.close()
   else:
      usage()

if __name__ == '__main__':
   main()

