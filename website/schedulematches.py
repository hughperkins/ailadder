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

# primarily for debugging, shows the count of the matches in the queue , or finished
# for each pair of ais

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

def go():
   leaguename = formhelper.getValue('leaguename')
   if leaguename == None:
      jinjahelper.message("Please select a league and try again")
      return

   if not loginhelper.isLoggedOn():   # this is pretty feeble, should make this a role...
      jinjahelper.message("Please log on first.")
      return

   league = leaguehelper.getLeague(leaguename)

   [success, matchrequestqueue] = gridclienthelper.getproxy().getmatchrequestqueuev1()
   [success, matchresults] = gridclienthelper.getproxy().getmatchresultsv1()

   ais = leaguehelper.getleagueais( league )

   matchscheduler.schedulematchesforleague( league, matchrequestqueue, matchresults )

   jinjahelper.message("Matches scheduled")

go()

sqlalchemysetup.close()

