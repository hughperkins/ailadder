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
import bz2
from optparse import OptionParser

try:
   import package_config
except:
   print "Please copy package_config.py.template to package_config.py, and personalize to your requirements."
   sys.exit(1)

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

sys.path.append( scriptdir + "/webserver/website" )

from utils import userinput, filehelper

# Package botrunner and website:

# creates bz2 archive at current directory, for relative filepath, called bz2tarfilename
def gitArchiveToBz2( relativefilepath, bz2tarfilename ):
   popen = subprocess.Popen( ["git", "archive", "HEAD@{0}", relativefilepath, "--format", "tar"], stdout = subprocess.PIPE)
   print "Creating git archive " + bz2tarfilename + " ..."
   (stdoutdata, stderrdata ) = popen.communicate(None)
   print " ... git archive finished ... waiting for bz2 ..."
   tarcontents = stdoutdata
   # tarcontents = popen.stdout.read()
   tarbz2contents = bz2.compress( tarcontents )
   fh = open( bz2tarfilename, "wb" )
   fh.write( tarbz2contents )
   fh.close()
   print " ... bz2 finished."

def gitAdd( filepath ):
      popen = subprocess.Popen( ["git", "add", filepath ] )
      popen.wait()   

def gitCommit(message):
   popen = subprocess.Popen( ["git", "commit", "-m", message ] )
   popen.wait()

def gitTag( tagname ):
   popen = subprocess.Popen( ["git", "tag", version ] )
   popen.wait()

def gitPush( destination ):
   popen = subprocess.Popen( ["git", "push", destination ] )
   popen.wait()

def gitPushBranch( destination, branch ):
   popen = subprocess.Popen( ["git", "push", destination, branch ] )
   popen.wait()

def scp( sourcefilepath, destinationfilepath ):
   popen = subprocess.Popen(['scp', sourcefilepath, destinationfilepath ])
   popen.wait()

# things to do:
# general:
# - get version from user
#
# package botrunner:
# - update botrunner/version.py
# - add botrunner/version.py to git
#
# package website:
# - update webserver/website/core/version.py
# - add webserver/website/core/version.py to git
#
# - commit git
# - push git to origin
#
# - git archive to packages/ailadder-botrunner-<version>.tar.bz2
# - git archive to packages/ailadder-website-<version>.tar.bz2

def go():
   optionparser = OptionParser()
   optionparser.add_option( '--dry-run', help = "don't commit anything to git", dest='dryrun', action='store_true')
   (options,args) = optionparser.parse_args()

   version = userinput.getValueFromUser("What version name do you want to you?")

   filehelper.writeFile( scriptdir + "/botrunner/version.py", "version = '" + version + "'\n" )
   filehelper.writeFile( scriptdir + "/webserver/website/core/version.py", "version = '" + version + "'\n" )

   if not options.dryrun:
      gitAdd( scriptdir + "/botrunner/version.py" )
      gitAdd( scriptdir + "/webserver/website/core/version.py" )
      gitCommit( "Updated botrunner version" )
      gitTag(version)
      gitPush('origin')
      gitPushBranch('origin', version)

   botrunnerpackagefilepath = scriptdir + '/packages/botrunner_' + version + ".tar.bz2"
   gitArchiveToBz2( scriptdir + '/botrunner', botrunnerpackagefilepath )

   websitepackagefilepath = scriptdir + '/packages/website_' + version + ".tar.bz2"
   gitArchiveToBz2( scriptdir + '/webserver', websitepackagefilepath )

   print "uploading botrunner package... "
   scp( botrunnerpackagefilepath, package_config.packagescpdestination )
   print " ... botrunner package uploaded"
   print "uploading website package... "
   scp( websitepackagefilepath, package_config.packagescpdestination )
   print " ... website package uploaded"

   print "Packages created at: "
   print package_config.packagewebsiteurl + "/botrunner_" + version + ".tar.bz2"
   print package_config.packagewebsiteurl + "/website_" + version + ".tar.bz2"

if __name__ == '__main__':
   go()


