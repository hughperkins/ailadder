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

import sqlalchemy
import tableclasses

try:
   import config
except:
   pass

engine = None
Session = None
session = None

def setupwithcredentials( rdbmsname, dbuser, dbpassword, dbhost, dbname ):
   global engine,Session,session

   engine = None
   if rdbmsname == None:
      rdbmsname = 'mysql'
   if rdbmsname == 'sqlite':
      engine = sqlalchemy.create_engine( 'sqlite:///' + dbname, echo=False)
   else:
      engine = sqlalchemy.create_engine( rdbmsname + '://' + dbuser + ":" + dbpassword + "@" + dbhost + "/" + dbname, echo=False)
   Session = sqlalchemy.orm.sessionmaker(bind=engine)
   session = Session()

def setup():
   global engine,Session,session

   setupwithcredentials( config.dbengine, config.dbuser, config.dbpassword, config.dbhost, config.dbname )

def close():
   session.commit()

def createalltables():
   global engine,Session,session
   tableclasses.createall(engine)
   tableclasses.addstaticdata(session)
   session.commit()

def dropalltables():
   global engine,Session,session
   tableclasses.dropall(engine)

def reloadalltables():
   global engine,Session,session
   dropalltables()
   createalltables()

