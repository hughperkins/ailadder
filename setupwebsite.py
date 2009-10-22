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

import sys
import os
import subprocess
import shutil

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

sys.path.append( scriptdir + "/website" )

from utils import userinput, filehelper

def checkpythonversion():
   if sys.version_info[0] > 2:
      print "Warning: tested with version 2.4, 2.5 or 2.6 of Python"
      return True

   if sys.version_info[0] < 2:
      print "You need version 2.4 or higher of Python"
      return False
      
   if sys.version_info[1] < 4:
      print "You need version 2.4 or higher of Python"
      return False

   print "...python version ok."
   print ""
   return True

# things we need to check:
# - python version
# - sqlalchemy installed?
# - if not:
#   - install globally?
#   - install on shared host?
def main():
   print ""
   print "AILadder website setup"
   print "======================"
   print ""

   print "Check python version..."
   if not checkpythonversion():
      return

   neededpackages = []

   print "Check sqlalchemy..."
   try:
      import sqlalchemy
      print "checked sqlalchemy: already installed.  Good."
   except:
      neededpackages.append('sqlalchemy')
      print "... need to install sqlalchemy"
   print ""

   print "Check jinja2..."
   try:
      import jinja2
      print "checked jinja2: already installed.  Good."
   except:
      neededpackages.append('jinja2')
      print "... need to install jinja2"
   print ""

   newpythonexecutable = None
   if len(neededpackages) > 0:
      print "We need to install some packages to run AILadder website."
      print "They can be installed globally, or in a virtual environment."
      print "If you are on a dedicated machine, global installation is probably best."
      print "If you are on a shared webhosting, you probably should use a virtual environment."
      installlocation = userinput.choice("Please choose target installation environment", { 'global': 'install globally', 'virtualenv': 'install to virtual environment' } )
      while installlocation == None:
         print "Please choose target installation environment:"
         print "g: install globally"
         print "v: install to a virtual environment."
         line = sys.stdin.readline().strip().lower()
         if line == 'g':
            installlocation = 'global'
         if line == 'v':
            installlocation = 'virtualenv'

      if installlocation == 'global':
         if 'sqlalchemy' in neededpackages:
            os.chdir(scriptdir + "/dependencies/SQLAlchemy-0.5.6")
            popen = subprocess.Popen([sys.executable, "setup.py","install"] )
            popen.wait()
         if 'jinja2' in neededpackages:
            os.chdir(scriptdir + "/dependencies/Jinja2-2.2.1")
            popen = subprocess.Popen([sys.executable, "setup.py","install"] )
            popen.wait()
      elif installlocation == 'virtualenv':
         virtualenvpath = ''
         while virtualenvpath == '':
            print "Please enter the path to the virtual env you wish to use or create:"
            virtualenvpath = sys.stdin.readline().strip()
            os.chdir(scriptdir + "/dependencies/virtualenv-1.3.4")
            popen = subprocess.Popen([sys.executable, "virtualenv.py", virtualenvpath] )
            popen.wait()
            newpythonexecutable = virtualenvpath + "/bin/python"

            if 'sqlalchemy' in neededpackages:
               os.chdir(scriptdir + "/dependencies/SQLAlchemy-0.5.6")
               popen = subprocess.Popen([newpythonexecutable, "setup.py","install"] )
               popen.wait()
            if 'jinja2' in neededpackages:
               os.chdir(scriptdir + "/dependencies/Jinja2-2.2.1")
               popen = subprocess.Popen([newpythonexecutable, "setup.py","install"] )
               popen.wait()

            print "Restarting in virtual environment..."
            popen = subprocess.Popen([newpythonexecutable, scriptdir + "/" + sys.argv[0] ], stdin = sys.stdin, stdout = sys.stdout )
            popen.wait()
            sys.exit(0)

   print ""
   print "Website installation"
   websitedir = ''
   while websitedir == '':
      print "Which directory do you wish to install the website to?"
      websitedir = sys.stdin.readline().strip()

   print "Copying website files..."
   if not os.path.exists(websitedir):
      os.makedirs(websitedir)
   for root, dirs, files in os.walk( scriptdir + "/website" ):
      reldir = root[len(scriptdir + "/website"):]
      #print reldir + " " + str(dirs) + " " + str(files)
      if not os.path.exists(websitedir + reldir):
         os.makedirs( websitedir + reldir )
      for file in files:
         shutil.copy( root + "/" + file, websitedir + reldir + "/" + file )
   if not os.path.exists(websitedir + "/replays"):
      os.makedirs(websitedir + "/replays")
   print " ... done"

   # replace path in .py files
   print "Updating #! path in website files..."
   targetpythonexecutable = sys.executable
   if newpythonexecutable != None:
      targetpythonexecutable = newpythonexecutable
   for file in os.listdir( websitedir ):
      if file.endswith(".py"):
         originalpyfile = filehelper.readFile( websitedir + "/" + file )
         originalpyfilelines = originalpyfile.split("\n")
         if originalpyfilelines[0].startswith("#!"):
            originalpyfilelines[0] = "#!" + targetpythonexecutable
            filehelper.writeFile( websitedir + "/" + file, "\n".join(originalpyfilelines) )
   print " ... done"

   print ""
   print "Database setup"
   print "=============="
   print ""
   dbengine = userinput.choice("Do you want to use mysql (needs mysql, recommended), or sqlite, for the website database?", {'mysql':'mysql','sqlite':'sqlite'} )

   configcontents = filehelper.readFile(websitedir + "/config.py.template" )
   dbuser = None
   dbpassword = None
   dbhost = None
   dbname = None
   if dbengine == 'sqlite':
      gotpath = False
      while not gotpath:
         print ""
         dbname = userinput.getValueFromUser("Please enter the full path to use for the sqlite database")
         print "checking if directory " + os.path.dirname( dbname ) + " exists..."
         if os.path.exists( os.path.dirname( dbname ) ):
            print " ... exists. Ok."
            gotpath = True
         else:
            print " ... does not exist."
      configcontents = configcontents.replace("DBENGINE",'sqlite')
      configcontents = configcontents.replace("DBNAME", dbname )
   elif dbengine == 'mysql':
      gotcredentials = False
      while not gotcredentials:
         print ""
         print "Please provide the name and host of a MySQL database that exists, and the username and password of a MySQL user with full write access to the database."
         dbuser = userinput.getValueFromUser("Please enter the database username")
         dbpassword = userinput.getValueFromUser("Please enter the database password")
         dbname = userinput.getValueFromUser("Please enter the database name")
         dbhost = userinput.getValueFromUser("Please enter the database hostname ('localhost' if it's on the same machine)")
         import sqlalchemy
         engine = sqlalchemy.create_engine('mysql://' + dbuser + ":" + dbpassword + "@" + dbhost + "/" + dbname )
         try:
            print "Checking connection to database..."
            connection = engine.connect()
            connection.close()
            print " ... succeeded"
            gotcredentials = True
         except:
            print " ... failed to connect to database"

      configcontents = configcontents.replace("DBENGINE", 'mysql' )
      configcontents = configcontents.replace("DBUSER", dbuser )
      configcontents = configcontents.replace("DBPASS", dbpassword )
      configcontents = configcontents.replace("DBHOST", dbhost )
      configcontents = configcontents.replace("DBNAME", dbname )

   filehelper.writeFile( websitedir + "/config.py", configcontents )

   print ""
   print "Populating database ..."
   from core import sqlalchemysetup
   sqlalchemysetup.setupwithcredentials( dbengine, dbuser, dbpassword, dbhost, dbname )
   sqlalchemysetup.reloadalltables()
   sqlalchemysetup.close()
   print " ... done"

   print ""
   print "This configuration completed."
   print ""
   print "Please do the following next:"
   print " - configure your webserver to host the " + websitedir + " directory"
   print " - ensure your website runs .py files in " + websitedir + " as Python in cgi"
   print " - ensure that " + websitedir + "/replays is writable by the webserver"
   print " - open the website in your web-browser to check all is ok."

if __name__ == '__main__':
   main()

