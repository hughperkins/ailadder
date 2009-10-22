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
import datetime

import sys
import os

from utils import *
from core import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

botrunners = sqlalchemysetup.session.query(BotRunner)

# if you know of a reliable way of just adding the following two data to  the business ojbects,
# go ahead:
botrunnerdata = {}
sessiondata = {}
for botrunner in botrunners:
   rowspan = 1
   if len(botrunner.sessions) > 1:
      rowspan = len(botrunner.sessions)
   botrunnerdata[botrunner] = {}
   botrunnerdata[botrunner]['rowspan'] = rowspan
   for session in botrunner.sessions:
      sessiondata[session] = {}
      sessiondata[session]['pingtimeok'] = False
      lastpingtimeddate = None
      lastpingtime =  session.lastpingtime
      if lastpingtime != None:
         lastpingtimedate = dates.dateStringToDateTime( lastpingtime )
         secondssincelastping = dates.timedifftototalseconds( datetime.datetime.now() - lastpingtimedate )
         sessiondata[session]['lastpingtimestring'] = str(lastpingtimedate)
         if secondssincelastping < confighelper.getValue('expiresessionminutes') * 60:
            session.pingtimeok = True
            sessiondata[session]['pingtimeok'] = True


jinjahelper.rendertemplate('viewbotrunners.html', botrunners = botrunners, isloggedin = loginhelper.isLoggedOn(), username = loginhelper.gusername, menus = menu.getmenus(), botrunnerdata = botrunnerdata, sessiondata = sessiondata )

sqlalchemysetup.close()

