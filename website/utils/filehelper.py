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

# return contents of filepath as string
def readFile( filepath ):
   filehandle = open( filepath, "r" )
   filecontents = ""
   line = filehandle.readline()
   while( line != "" ):
      filecontents = filecontents + line
      line = filehandle.readline()
   filehandle.close()
   return filecontents

# write contents string to filepath
def writeFile( filepath, contents ):
   filehandle = open( filepath, "w" )
   filehandle.write( contents )
   filehandle.close()

def test():
   teststring = u"blah\nfoo\nhello world!T^*6789"
   filepath = "/tmp/foo.txt"
   writeFile( filepath, teststring )
   newstring = readFile( filepath )
   if newstring != teststring:
      print "FAIL"
      return

   print "PASS"


if __name__ == "__main__":
   test()


