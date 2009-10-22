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

# lets a user add a single account to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

sqlalchemysetup.setup()

loginhelper.processCookie()

def go():
   if not loginhelper.isLoggedOn():
      jinjahelper.message( "Please log in first." )
      return

   oldpassword = formhelper.getValue('oldpassword')
   password = formhelper.getValue('password')
   confirmpassword = formhelper.getValue('confirmpassword')

   if password == None or confirmpassword == None or password == '' or confirmpassword == '' or oldpassword == None or oldpassword == '':
      jinjahelper.message( "Please fill in the fields and try again" )
      return

   if password != confirmpassword:
      jinjahelper.message( "Confirmation password doesn't match new password" )
      return
      
   # check oldpassword
   if not loginhelper.validateUsernamePassword( loginhelper.getUsername(), oldpassword ):
      jinjahelper.message( "Please check your old password and try again" )
      return

   if loginhelper.changePassword( loginhelper.getUsername(), password ):
      jinjahelper.message( "Password changed ok" )
   else:
      jinjahelper.message( "Something went wrong.  Please check your values and try again." )

go()

sqlalchemysetup.close()


