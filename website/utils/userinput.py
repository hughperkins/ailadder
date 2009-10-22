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

import sys

# returns True for confirmed, otherwise False
def getConfirmation( confirmationquestion ):
   print confirmationquestion + " (y to confirm)"
   confirmation = sys.stdin.readline().strip().lower()
   if confirmation == 'y':
      return True
   return False

# returns the entered file path or ""
def askForPathToFile( pathName ):
   while True:
      print "Please enter the full path to " + pathName + ":"
      thePath = sys.stdin.readline().strip()
      if os.path.exists(thePath):
         return thePath
      else:
         print "The specified file \"" + thePath + "\" does not exist, please try again."
         continue
   return ''

def getValueFromUser(questiontouser):
   while True:
      print questiontouser
      inputline = sys.stdin.readline()
      uservalue = inputline.strip()
      if uservalue != '':
         return uservalue

def choice( question, optiondict ):
   while True:
      print question
      for i in xrange(len(optiondict)):
         print str(i + 1) + ". " + optiondict.values()[i]
      userentry = sys.stdin.readline().strip().lower()
      try:
         userindex = int( userentry )
         if userindex < 1 or userindex > len(optiondict) + 1:
            print "Please enter a number between 1 and " + str( len(optiondict) + 1 )
         return optiondict.keys()[ userindex - 1]
      except:
         print "Please enter a number between 1 and " + str( len(optiondict) + 1 )

def getPath( pathname, potentialpaths ):
   # just include paths that exist
   paths = []
   for potentialpath in potentialpaths:
      if os.path.exists( potentialpath ):
         paths.append( potentialpath )

   print paths
   while True:
      print "Please enter the number of the path to " + pathname + ":"
      for i in xrange( len( paths ) ):
         print str(i + 1 ) + ". " + paths[i]
      print str( len( paths ) + 1 ) + ". custom path (eg " + potentialpaths[0] + ")"

      inputline = sys.stdin.readline().strip()
      if inputline == '':
         continue
      try:
         index = int( inputline )
      except:
         # user didn't enter a number
         # could be a path?
         try:
            if not os.path.exists( inputline ):
               print "Not a valid path for " + pathname
               continue
            return inputline
         except:
            # probably not a spring executable
            print "Not a valid path for " + pathname
            continue
         
      if index < 1 or index > len( paths ) + 1:
         print "Please enter a number from 1 to " + str( len( paths ) + 1 ) + "."
         continue
      if index <= len( paths ):
         return paths[index - 1]
      # user wants to enter a custom path:
      print "Please type in the path to " + pathname + " (eg " + potentialpaths[0] + ") :"
      inputline = sys.stdin.readline().strip()
      if inputline == '':
         continue
      if not os.path.exists( inputline ):
         print "Not a valid path for " + pathname
         continue
      return inputline


