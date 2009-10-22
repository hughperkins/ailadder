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

# lets a user add a single mod to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

if not roles.isInRole(roles.modadmin):
   jinjahelper.message( "You must be logged in as a modadmin" )
else:
   modname = formhelper.getValue("modname")
   modarchivechecksum = formhelper.getValue("modarchivechecksum")
   modurl = formhelper.getValue("modurl")

   if modname != None and modname != "" and modarchivechecksum != None and modarchivechecksum != '':
      if modurl == None:
         modurl = ''
      mod = Mod( modname, modarchivechecksum )
      mod.modurl = modurl
      sqlalchemysetup.session.add( mod )
      sqlalchemysetup.session.commit()
      jinjahelper.message( "Added ok" )
   else:
      jinjahelper.message( "Please fill in the fields and try again" )

sqlalchemysetup.close()
\