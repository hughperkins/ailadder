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

import cgi
import os
import base64
import sys

# helps with form stuff

# Generator to buffer file chunks
# This function from http://webpython.codepoint.net/cgi_big_file_upload
def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

form = None

def getform():
   global form
   if form == None:
      form = cgi.FieldStorage()
   return form

# you can run from commandline too, in format:
# python somescript.py fieldname=fieldvalue ...
def getValue( fieldname ):
   form = getform()
   if not form.has_key(fieldname):
      for arg in sys.argv:
         if arg.startswith(fieldname):
            return arg.split('=')[1]
      return None
   return form[fieldname].value

# takes a file at fieldname
# and writes it to disk at outputpath
# returns true if succeeds
# or false if no such field item
def writeIncomingFileToDisk( fieldname, outputpath ):
   filebase64 = getValue(fieldname)
   if filebase64 == None:
      print "no replay field detected in incoming post"
      return False # file not uploaded

   print "base64length: " + str( len( filebase64 ) ) + "<br />"
   filebinary = base64.decodestring( filebase64 )
   print "binlength: " + str( len( filebinary ) ) + "<br />"

   # print "output path: " + outputpath
   outputfilehandle = open(outputpath, 'wb' )
   outputfilehandle.write(filebinary)
   outputfilehandle.close()
   return True


