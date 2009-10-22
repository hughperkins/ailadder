#!/usr/bin/python

# Copyright Hugh Perkins 2004, 2009
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

import datetime

import stringhelper

# datestrings are in format:
# yyyymmddhhmmss
#

def dateStringToDateTime( datestring ):
   # strptime is not available on older versions of python, so rewrite...
   # return datetime.datetime.strptime(datestring,"%Y%m%d%H%M%S")
   (year, datestring ) = stringhelper.eatAsInt(datestring, 4 ) 
   (month, datestring ) = stringhelper.eatAsInt(datestring, 2 ) 
   (day, datestring ) = stringhelper.eatAsInt(datestring, 2 ) 
   (hour, datestring ) = stringhelper.eatAsInt(datestring, 2 ) 
   (minute, datestring ) = stringhelper.eatAsInt(datestring, 2 ) 
   (second, datestring ) = stringhelper.eatAsInt(datestring, 2 ) 
   return datetime.datetime( year, month, day, hour, minute, second )

def dateTimeToDateString( datedatetime ):
   return datedatetime.strftime("%Y%m%d%H%M%S")

def timedifftototalseconds( timediff ):
   return timediff.days * 24 * 3600 + timediff.seconds

# self test function
def test():
   somedate = datetime.datetime(2009,5,3,2,6,17)
   print somedate
   datestring = dateTimeToDateString( somedate )
   print datestring
   if datestring != "20090503020617":
      print 'FAIL'
      return
   seconddate = dateStringToDateTime( datestring )
   print seconddate
   if seconddate != somedate:
      print 'FAIL'
      return
   print 'PASS'

if __name__ == '__main__':
   test()

