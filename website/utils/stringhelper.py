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

import string
import random

# eats first n chars of string, and returns as int
def eatAsInt( targetstring, n ):
   intstring = targetstring[0:n]
   #print intstring
   remainingstring = targetstring[n:]
   #print remainingstring
   return ( int(intstring), remainingstring )

def getRandomAlphaNumericString(length):
   randomstring = ''
   alphanumericchars = string.letters + string.digits
   while len(randomstring) < length:
      randomstring = randomstring + alphanumericchars[random.randrange(0,len(alphanumericchars))]
   return randomstring

def getRandomPrintableString(length):
   randomstring = ''
   while len(randomstring) < length:
      randomstring = randomstring + string.printable[random.randrange(0,len(string.printable))]
   return randomstring

def getRandomString(length):
   if length == 0:
      return ''
   return string.letters[random.randrange(0,52)] + getRandomString( length - 1 )

# self test function
def test():
   startstring = "200904"
   (intvalue, startstring) = eatAsInt( startstring, 4 )
   print intvalue
   if intvalue != 2009:
      print "FAIL"
      return
   (intvalue, startstring) = eatAsInt( startstring, 2 )
   print intvalue
   if intvalue != 4:
      print "FAIL"
      return
   print 'PASS'

if __name__ == '__main__':
   test()


