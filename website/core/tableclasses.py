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

import md5

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, and_, schema, Table
from sqlalchemy.orm import backref, relation

from utils import *
import loginhelper

Base = sqlalchemy.ext.declarative.declarative_base()

class Role(Base):
   __tablename__ = 'roles'

   def __init__(self, role_name ):
      self.role_name = role_name

   role_id = Column(Integer,primary_key=True)
   role_name = Column(String(255), unique = True, nullable = False)

account_roles = Table('role_members', Base.metadata,
   Column('role_id', Integer,ForeignKey('roles.role_id'),nullable=False),
   Column('account_id', Integer,ForeignKey('accounts.account_id'),nullable=False),
   UniqueConstraint('role_id','account_id')
)

class Account(Base):
   __tablename__ = 'accounts'

   account_id = Column(Integer,primary_key=True)
   username = Column(String(255), unique = True, nullable = False)
   userfullname = Column(String(255))
   useremailaddress = Column(String(255))
   passwordsalt = Column(String(255), nullable = False)
   passwordhash = Column(String(255), nullable = False)

   roles = relation("Role", secondary = account_roles )

   def __init__(self, username, userfullname, password ):
      self.username = username
      self.userfullname = userfullname

      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( password + self.passwordsalt ).hexdigest()

   def checkPassword( self, password ):
      return ( md5.md5( password + self.passwordsalt ).hexdigest() == self.passwordhash )

   def changePassword( self, newpassword ):
      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( newpassword + self.passwordsalt ).hexdigest()

   def addRole( self, role ):
      self.roles.append(role)

class AIAllowedMap(Base):
   __tablename__ = 'ai_allowedmaps'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   map_name = Column(String(255),primary_key=True)

   ai = relation("AI")

class AIAllowedMod(Base):
   __tablename__ = 'ai_allowedmods'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   mod_name = Column(String(255),primary_key=True)

   ai = relation("AI")

ai_allowedoptions = Table('ai_allowedoptions', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ais.ai_id'),nullable = False ),
   Column('option_id',Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('ai_id', 'option_id')
)

class AI(Base):
   __tablename__ = 'ais'

   ai_id = Column(Integer,primary_key=True)
   ai_name = Column(String(255), nullable = False)
   ai_version = Column(String(255), nullable = False)
   ai_downloadurl = Column(String(255))
   ai_owneraccount_id = Column(Integer,ForeignKey('accounts.account_id'))

   __table_args__ = (schema.UniqueConstraint('ai_name','ai_version'), {} )

   allowedmaps = relation("AIAllowedMap")
   allowedmods = relation("AIAllowedMod")
   allowedoptions = relation("AIOption", secondary = ai_allowedoptions)

   owneraccount = relation("Account")

   def __init__( self, ai_name, ai_version ):
      self.ai_name = ai_name
      self.ai_version = ai_version

class Cookie(Base):
   __tablename__ = 'cookies'

   def __init__( self, cookiereference, account ):
      self.cookiereference = cookiereference
      self.account = account

   cookiereference = Column(String(255),primary_key=True)
   #username = Column(String(255))
   # we can change to use account_id in the future
   account_id = Column(Integer,ForeignKey('accounts.account_id'), nullable = False)

   account = relation("Account")

class AIOption(Base):
   __tablename__ = 'aioptions'

   option_id = Column(Integer,primary_key=True)
   option_name = Column(String(255), unique = True, nullable = False)

   def __init__(self, option_name):
      self.option_name = option_name

leagueoptions = Table( 'leagueoptions', Base.metadata,
   Column('league_id', Integer,ForeignKey('leagues.league_id'),nullable = False),
   Column('option_id', Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('league_id', 'option_id')
)

class League(Base):
   __tablename__ = 'leagues'

   league_id = Column(Integer,primary_key = True )
   league_name = Column(String(255), unique= True, nullable = False)
   league_creatorid = Column(Integer,ForeignKey('accounts.account_id'))
   map_name = Column(String(255), nullable = False)
   mod_name = Column(String(255), nullable = False)
   nummatchesperaipair = Column(Integer, nullable = False)

   creator = relation("Account")
   options = relation("AIOption", secondary = leagueoptions )

   def __init__( self, league_name, creator, mod_name, map_name, nummatchesperaipair ):
      self.league_name = league_name
      self.creator = creator
      self.mod_name = mod_name
      self.map_name = map_name
      self.nummatchesperaipair = nummatchesperaipair

# members who are leaguegruops
leaguegroup_leaguemembers = Table( 'leaguegroup_leaguemembers', Base.metadata,
   Column('leaguegroup_id', Integer,ForeignKey('leaguegroups.leaguegroup_id'),nullable = False),
   Column('league_id', Integer,ForeignKey('leagues.league_id'),nullable = False),
   UniqueConstraint('leaguegroup_id', 'league_id')
)

# add this later ;-)
#leaguegroup_leaguegroupmembers = Table( 'leaguegroup_leaguegroupmembers', Base.metadata,
#   Column('leaguegroup_id', Integer,ForeignKey('leaguegroups.leaguegroup_id'),nullable = False),
#   Column('childleaguegroup_id', Integer,ForeignKey('leaguegroups.leaguegroup_id'),nullable = False),
#   UniqueConstraint('leaguegroup_id', 'childleaguegroup_id')
#)

class LeagueGroup(Base):
   __tablename__ = 'leaguegroups'

   leaguegroup_id = Column(Integer,primary_key = True)
   leaguegroup_name = Column(String(255), unique = True, nullable = False)
   leaguegroup_creatorid = Column(Integer,ForeignKey("accounts.account_id"))
   
   creator = relation("Account")
   childleagues = relation("League", secondary = leaguegroup_leaguemembers )
   # childleaguegroups = relation("LeagueGroup", secondary = leaguegroup_leaguegroupmembers )

   def __init__( self, leaguegroup_name ):
      self.leaguegroup_name = leaguegroup_name

# simple flat config for now
class Config(Base):
   __tablename__ = 'config'

   config_key = Column(String(255),primary_key = True )
   config_value = Column(String(255), nullable = False)
   config_type = Column(String(255), nullable = False)

   # sets value of config_type appropriately, according to config_value type
   # to int, float, string or boolean
   def __init__(self, config_key, config_value ):
      self.config_key = config_key
      self.setValue( config_value )

   def setValue( self, config_value ):
      self.config_value = str(config_value)
      if type(config_value) == int:
         self.config_type = 'int'
      elif type(config_value) == float:
         self.config_type = 'float'
      elif type(config_value) == str:
         self.config_type = 'string'
      elif type(config_value) == bool:
         self.config_type = 'boolean'

   # returns config_value converted into appropriate type, according t o value of config_type
   def getValue(self):
      if self.config_type == 'int':
         return int(self.config_value)
      if self.config_type == 'float':
         return float(self.config_value)
      if self.config_type == 'string':
         return self.config_value
      if self.config_type == 'boolean':
         if self.config_value.lower() == 'true':
            return True
         return False
      
def addstaticdata(session):
   import confighelper # have to import it here, otherwise Config table can't be easily
                       # imported inside confighelper, because circular import loop
   confighelper.applydefaults()

   # maybe roles static data could be created by core/roles.py?
   # anyway, for now... :
   accountadminrole = Role("accountadmin")
   aiadminrole = Role("aiadmin")
   modadminrole = Role("modadmin")
   mapadminrole = Role("mapadmin")
   leagueadminrole = Role("leagueadmin")

   session.add(accountadminrole)
   session.add(aiadminrole)
   session.add(modadminrole)
   session.add(mapadminrole)
   session.add(leagueadminrole)

   account = Account("admin","admin", "admin")
   session.add(account)
   account.addRole( accountadminrole )
   account.addRole( aiadminrole )
   account.addRole( modadminrole )
   account.addRole( mapadminrole )
   account.addRole( leagueadminrole )

   session.add(Account("guest","guest","guest"))

   aioption_cheatingequalslose = AIOption('cheatingequalslose')
   aioption_cheatingallowed = AIOption('cheatingallowed')
   aioption_dummymatch = AIOption('dummymatch')
   session.add(aioption_cheatingequalslose)
   session.add(aioption_cheatingallowed)
   session.add(aioption_dummymatch)

def createall(engine):
   Base.metadata.create_all(engine)

def dropall(engine):
   Base.metadata.drop_all(engine)



