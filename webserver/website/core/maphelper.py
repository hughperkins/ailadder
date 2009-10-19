# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or mapify it
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

from utils import *
import sqlalchemysetup
from tableclasses import *
import botrunnerhelper

# returns True if exists, or added ok, otherwise False
def addmapifdoesntexist(mapname, maparchivechecksum):
   map = sqlalchemysetup.session.query(Map).filter(Map.map_name == mapname ).first()
   if map == None:
      try:
         map = Map( mapname, maparchivechecksum )
         sqlalchemysetup.session.add(map)
         sqlalchemysetup.session.commit()
      except:
         return(False, "error adding to db: " + str( sys.exc_value ) )

      return (True,'')

   if map.map_archivechecksum != maparchivechecksum:
      return (False,"map archive checksum doesn't match the one already on the website.")

   return (True,'')

def getMap( mapname ):
   return sqlalchemysetup.session.query(Map).filter(Map.map_name == mapname ).first()

# return list of supported mapnames
def getsupportedmaps( botrunnername ):
   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   if botrunner == None:
      return []
   if botrunner.supportedmaps == None:
      return []
   supportedmapnames = []
   for map in botrunner.supportedmaps:
      supportedmapnames.append(map.map.map_name)
   return supportedmapnames

def setbotrunnersupportsthismap( botrunnername, mapname ):
   # Now, register the map as supported map
   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   for map in botrunner.supportedmaps:
      if map.map.map_name == mapname:
       return (True,'')
   map = getMap(mapname)
   botrunner.supportedmaps.append(BotRunnerSupportedMap(map))
   sqlalchemysetup.session.commit()
   return (True,'')

