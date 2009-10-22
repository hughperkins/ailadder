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

import cgitb; cgitb.enable()

from sqlalchemy.orm import join

from utils import *
from core import *

sqlalchemysetup.setup()

loginhelper.processCookie()

leaguename = formhelper.getValue('leaguename')

compatibleoptions = listhelper.tuplelisttolist(
   sqlalchemysetup.session.query( tableclasses.AIOption.option_name )
      .select_from(join(join(tableclasses.AIOption,tableclasses.LeagueOption),tableclasses.League))
      .filter(tableclasses.League.league_name == leaguename ) )

showform = roles.isInRole(roles.leagueadmin)

potentialoptions = listhelper.tuplelisttolist(
   sqlalchemysetup.session.query(tableclasses.AIOption.option_name ) )
for assignedoption in compatibleoptions:
   potentialoptions.remove(assignedoption)

jinjahelper.rendertemplate('viewleague.html', leaguename = leaguename, compatibleoptions = compatibleoptions, showform = showform, potentialoptions = potentialoptions )

sqlalchemysetup.close()

