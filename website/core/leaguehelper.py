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

import sqlalchemysetup
from tableclasses import *

def getLeague( league_name ):
   return sqlalchemysetup.session.query(League).filter( League.league_name == league_name ).first()

def getLeagueGroup( leaguegroup_name ):
   return sqlalchemysetup.session.query(LeagueGroup).filter( LeagueGroup.leaguegroup_name == leaguegroup_name ).first()

# return only ais that comply with league conditions
def getleagueais( league ):
   ais = sqlalchemysetup.session.query(AI).all()
   ailist = []

   for ai in ais:
      aihasalloptions = True
      for leagueoption in league.options:
         aihasthisoption = False
         for aioption in ai.allowedoptions:
            if aioption.option.option_name == leagueoption.option.option_name:
               aihasthisoption = True
         if not aihasthisoption:
            aihasalloptions = False
      if aihasalloptions:
         ailist.append(ai)

   return ailist
   

