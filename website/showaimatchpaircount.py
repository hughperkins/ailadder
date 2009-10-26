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
   leaguenames = listhelper.tuplelisttolist( sqlalchemysetup.session.query( League.league_name ) )
   if len(leaguenames) == 0:
      jinjahelper.message("Please create a league first.")
      return

   leaguename = formhelper.getValue('leaguename')
   if leaguename == None:
      leaguename = leaguenames[0]

   league = leaguehelper.getLeague(leaguename)

   gridais = gridclienthelper.getproxy().getais()

   for gridai in gridais:
      aihelper.addaiifdoesntexist( gridai['ai_name'], gridai['ai_version'] )
   sqlalchemysetup.session.flush()

   ais = leaguehelper.getleagueais( league )

   [success, matchrequestqueue] = gridclienthelper.getproxy().getmatchrequestqueuev1()
   [success, matchresults] = gridclienthelper.getproxy().getmatchresultsv1()
   [success, mapok ] = gridclienthelper.getproxy().mapexists( league.map_name )
   #if not mapok:
   #   jinjahelper.message("League " + leaguename + " uses a currently unavailable map: " + league.map_name)
   #   return
   [success, modok ] = gridclienthelper.getproxy().modexists( league.mod_name )
   #if not modok:
   #   jinjahelper.message("League " + leaguename + " uses a currently unavailable mod: " + league.mod_name)
   #   return

   indextoai = matchscheduler.getindextoai(league)
   aipairqueuedmatchcount = matchscheduler.getaipairmatchcount( matchrequestqueue,league, ais, indextoai )
   aipairfinishedcount = matchscheduler.getaipairmatchcount( matchresults,league, ais, indextoai )

   showform = loginhelper.isLoggedOn()

   jinjahelper.rendertemplate( 'showaimatchpaircount.html', aipairqueuedmatchcount = aipairqueuedmatchcount, aipairfinishedcount = aipairfinishedcount, indextoai = indextoai, ais = ais, leaguenames = leaguenames, league = league, numais = len(ais), nummatchesperaipair = league.nummatchesperaipair, mapok = mapok, modok = modok, showform = showform )

go()

sqlalchemysetup.close()

