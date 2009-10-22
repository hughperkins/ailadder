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

# This is basically used for debug
# It pumps a single request into the queue
# Once there are other systems in place, this file will either be purged, moved
# elsewhere, or protected by some admin authentication system
# for now, no authentication...

# also, no form for now, we just put the request into the querystring ;-)

import cgitb; cgitb.enable()
import sys
import os
import Cookie
# import cookiefile
import cgi

import config

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

def checkformvarsnotnonenotempty( vars ):
   failed = []
   for var in vars:
      if formhelper.getValue(var) == None or formhelper.getValue(var) == '':
         failed.append(var)
   return [ len(failed) == 0, failed ]

def go():
   if not loginhelper.isLoggedOn():
      jinjahelper.message( "Please login first." )
      return

   [result, missingfields ] = checkformvarsnotnonenotempty(['ai0nameversion', 'ai1nameversion', 'mapname', 'modname'])
   if not result:
      jinjahelper.message("Please fill in all the fields.  Missing " + ",".join(missingfields) )
      return

   ai0nameversion = formhelper.getValue("ai0nameversion")
   ai0name = ai0nameversion.split("|")[0]
   ai0version = ai0nameversion.split("|")[1]
   ai1nameversion = formhelper.getValue("ai1nameversion")
   ai1name = ai1nameversion.split("|")[0]
   ai1version = ai1nameversion.split("|")[1]
   mapname = formhelper.getValue("mapname")
   modname = formhelper.getValue("modname")

   [success, errormessage ] = gridclienthelper.getproxy().schedulematchv1( mapname, modname, [ { 'ai_name': ai0name, 'ai_version': ai0version }, { 'ai_name': ai1name, 'ai_version': ai1version } ], [] ) 

   if success:
      jinjahelper.message( "Submitted ok." )
   else:
      jinjahelper.message( errormessage )

try:
   go()
except:
   jinjahelper.message( "An unexpected error occurred: " + str(sys.exc_info() ) )

sqlalchemysetup.close()

