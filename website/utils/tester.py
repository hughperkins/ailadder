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

# maybe there is some standard junit type thing for python (pyunit perhaps?)
# anyway, for now, until someone points out the standard way of doing this

def testBoolean( description, testvalue, targetvalue ):
   if testvalue == targetvalue:
      print "Testing " + description + ": PASS"
      return True
   else:
      print "Testing " + description + ": FAIL: " + str(testvalue) + " vs " + str(targetvalue)
      return False

# self test function
def test():
   if testBoolean("check for true", True, True ) == False:
      print 'FAIL'
      return
   if testBoolean("check for true", False, False ) == False:
      print 'FAIL'
      return
   if testBoolean("check for false, should print FAIL", True, False ) == True:
      print 'FAIL'
      return
   if testBoolean("check for false, should print FAIL", False, True ) == True:
      print 'FAIL'
      return
   print 'PASS'

