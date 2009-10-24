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

# This could ideally be converted to static methods on Config class, once 
# I have an internet connectoin and can google for how to do that ;-)

import sqlalchemysetup
from tableclasses import *

defaults = {
   'guimarksessionasmaybedownafterthismanyminutes': 6
} 

def getKeys():
   keys = []
   for config in sqlalchemysetup.session.query(Config):
      keys.append(config.config_key)
   return keys

def applydefaults():
   global defaults
   for key_name in defaults.keys():
      configrow = sqlalchemysetup.session.query(Config).filter(Config.config_key == key_name).first()
      if configrow == None:
         setValue( key_name, defaults[key_name] )         

# adds default for this value, and populates row in the database
def populatedefault(key_name):
   global defaults
   configrow = sqlalchemysetup.session.query(Config).filter(Config.config_key == key_name).first()
   if configrow != None:
      return configrow.getValue()

   if not defaults.has_key(key_name):
      return None
   newvalue = defaults[key_name]

   setValue( key_name, newvalue )
   return newvalue

# get an appropriately typed config value, indexed by key_name
def getValue( key_name ):
   configrow = sqlalchemysetup.session.query(Config).filter(Config.config_key == key_name ).first()
   if configrow == None:
      return populatedefault(key_name)
   return configrow.getValue()

def setValue(key_name, key_value):
   configrow = sqlalchemysetup.session.query(Config).filter(Config.config_key == key_name ).first()
   if configrow == None:
      config = Config(key_name, key_value)
      sqlalchemysetup.session.add(config)
   else:
      configrow.setValue( key_value)

