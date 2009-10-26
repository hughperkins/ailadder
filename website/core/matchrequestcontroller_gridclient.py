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

# This contains code for manipulating the matchrequest, via the gridclient proxy

import datetime

from sqlalchemy.orm import join

from utils import *
#from core import *
from tableclasses import *
import sqlalchemysetup
import botrunnerhelper
import confighelper
import gridclienthelper

# returns the new match request, so can add options and so on
# doesn't commit
def addmatchrequest( ai0, ai1, mod_name, map_name, league = None ):
   [result, message] = gridclienthelper.getproxy().schedulematchv1(map_name,mod_name,[{'ai_name': ai0.ai_name,'ai_version': ai0.ai_version},{'ai_name': ai1.ai_name, 'ai_version': ai1.ai_version } ],[])
   if not result:
      print "error: " + message
      raise Exception(message)



