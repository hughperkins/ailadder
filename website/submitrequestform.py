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

# creates a form to submit a single game request
# this won't be used later on, but it's good for getting the site started
# with something that works

# we'll load the available ai names, versions, maps, and mods
# from the database, to make it easy to use

import cgitb; cgitb.enable()

from utils import *
from core import *

sqlalchemysetup.setup()

ais = sqlalchemysetup.session.query( tableclasses.AI.ai_name, tableclasses.AI.ai_version )
maps = listhelper.tuplelisttolist( sqlalchemysetup.session.query( tableclasses.Map.map_name ) )
mods = listhelper.tuplelisttolist( sqlalchemysetup.session.query( tableclasses.Mod.mod_name ) )

options = listhelper.tuplelisttolist( sqlalchemysetup.session.query( tableclasses.AIOption.option_name ) )

aiitems = []
aivalues = []
for ai in ais:
   aivalues.append( ai.ai_name + " " + ai.ai_version )
   aiitems.append( ai.ai_name + "|" + ai.ai_version )

jinjahelper.rendertemplate('submitrequestform.html', ais = ais, maps = maps, mods = mods, aivalues = aivalues, aiitems = aiitems, options = options )

sqlalchemysetup.close()

