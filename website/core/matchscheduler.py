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

# The job of this module is to schedule matches for the various leagues.

# For now, initial first implementation, we will do the following:
# - for each league, take all ais
# - pair up
# - for each pair, check that the matchrequest table contains at least nummatchesperaipair
#   matches
# - otherwise schedule new ones

from tableclasses import *
import sqlalchemysetup
import leaguehelper
import aihelper
import matchrequestcontroller

# does for one league
def schedulematchesforleague( leaguename ):
   league = leaguehelper.getLeague(leaguename)
   ais = aihelper.getAIs()
   [ aitoindex, indextoai ] = getaiindexes(ais)
   aipairmatchcount = getaipairmatchcount(sqlalchemysetup.session.query( MatchRequest ), league, ais, aitoindex)
   for outerai in ais:
      for innerai in ais:
         if aipairmatchcount[aitoindex[outerai]][aitoindex[innerai]] < league.nummatchesperaipair:
            for i in xrange( league.nummatchesperaipair - aipairmatchcount[aitoindex[outerai]][aitoindex[innerai]] ):
               scheduleleaguematch( league, outerai, innerai )
            aipairmatchcount[aitoindex[outerai]][aitoindex[innerai]] = league.nummatchesperaipair
            aipairmatchcount[aitoindex[innerai]][aitoindex[outerai]] = league.nummatchesperaipair

def scheduleleaguematch( league, ai0, ai1 ):
   matchrequestcontroller.addmatchrequest( ai0 = ai0, ai1 = ai1, map = league.map, mod = league.mod, league = league )

# returns [ dict from ai to zero-based aiindex, dict from index to ai ]
def getaiindexes(ais):
   # assume this query is cached in memory, so fine to redo
   aitoindex = {}  # dict from ai to aiindex
   indextoai = {} # dict from index to ai
   for ai in ais:
      aitoindex[ ai ] = len(aitoindex)
      indextoai[ len(indextoai) ] = ai
   return [ aitoindex, indextoai ]

# return 2d list ([][]), indexed by indexes returned by getaiindexes
# showing the numer of matches in the queue between each pair of ais
# have to pass in requests one wants to consider
# that means one can pass in all requests, or just finished, or just not finished
# etc...
def getaipairmatchcount(requests, league, ais, aitoindex ):
   # go through each matchrequest in the queue, and increment matchcountarray member
   # we go through all requests that match the league: both the ones that have results, and the ones 
   # that don't
   matchcountarray = []  # 2d array of count of matches from one ai to another
   # build up empty array
   for outerai in ais:
      thisline = []
      matchcountarray.append(thisline)
      for innerai in ais:
         thisline.append(0)
   for matchrequest in requests:
      if matchrequest.map != league.map:
         continue
      if matchrequest.mod != league.mod:
         continue
      ai0index = aitoindex[matchrequest.ai0]
      ai1index = aitoindex[matchrequest.ai1]
      # add both ways around
      matchcountarray[ai0index][ai1index] = matchcountarray[ai0index][ai1index] + 1
      if ai0index != ai1index:
         matchcountarray[ai1index][ai0index] = matchcountarray[ai1index][ai0index] + 1
   return matchcountarray

# does for all leagues
def schedulematches():
   for league in sqlalchemysetup.session.query(League):
      schedulematchesforleague(league.league_name )

