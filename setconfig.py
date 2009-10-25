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

# intended to be called from the commandline

import sys
import os

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

sys.path.append( scriptdir + "/website" )

from core import *

def go():
   sqlalchemysetup.setup()
   if len(sys.argv) < 3:
      print "Usage: " + sys.argv[0] + " [keyname] [string|integer|float|boolean] [keyvalue]"
      return

   key = sys.argv[1]
   type = sys.argv[2]
   value = sys.argv[3]
   if type == 'float':
      value = float(value)
   if type == 'boolean':
      if value.lower() == 'true' or value.lower() == 'yes':
         value = True
      else:
         value = False
   if type == 'integer':
      value = int(value)

   confighelper.setValue( key, value )
          
   sqlalchemysetup.close()

go()

