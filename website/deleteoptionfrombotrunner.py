#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or aiify it
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

# lets a user add a single ai to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

def go():
   botrunnername = formhelper.getValue('botrunnername')
   optionname = formhelper.getValue('optionname')

   if not loginhelper.isLoggedOn():
      jinjahelper.message( "Please logon first." )
      return

   if botrunnername == None or optionname == None or botrunnername == '' or optionname == '':
      jinjahelper.message( "Please fill in the fields and try again" )
      return

   botrunnerownername = botrunnerhelper.getOwnerUsername( botrunnername ) 
   if botrunnerownername != loginhelper.getUsername() and not roles.isInRole( roles.botrunneradmin ):
      jinjahelper.message( "You must be the botrunner owner or a botrunneradmin" )
      return

   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   for option in botrunner.options:
      if option.option.option_name == optionname:
         sqlalchemysetup.session.delete( option )

   jinjahelper.message( "Removed ok" )

go()

sqlalchemysetup.close()

