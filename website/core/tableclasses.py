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

from sqlalchemy import Column, String, Integer, ForeignKey, and_
from sqlalchemy.orm import backref, relation

from utils import *
import loginhelper

Base = sqlalchemy.ext.declarative.declarative_base()

class Map(Base):
   __tablename__ = 'maps'

   map_id = Column(Integer,primary_key=True)
   map_name = Column(String(255))
   map_archivechecksum = Column(String(255))
   map_url = Column(String(255))

   def __init__(self, map_name, map_archivechecksum ):
      self.map_name = map_name
      self.map_archivechecksum = map_archivechecksum

class Mod(Base):
   __tablename__ = 'mods'

   mod_id =Column(Integer,primary_key=True)
   mod_name = Column(String(255))
   mod_archivechecksum = Column(String(255))
   mod_url = Column(String(255))

   def __init__(self, mod_name, mod_archivechecksum ):
      self.mod_name = mod_name
      self.mod_archivechecksum = mod_archivechecksum

class Role(Base):
   __tablename__ = 'roles'

   def __init__(self, role_name ):
      self.role_name = role_name

   role_id = Column(Integer,primary_key=True)
   role_name = Column(String(255))

class RoleMember(Base):
   __tablename__ = 'role_members'

   role_id = Column(Integer,ForeignKey('roles.role_id'),primary_key=True)
   account_id = Column(Integer,ForeignKey('accounts.account_id'),primary_key=True)

   role = relation("Role")

   def __init__(self, role ):
      self.role = role

class Account(Base):
   __tablename__ = 'accounts'

   account_id = Column(Integer,primary_key=True)
   username = Column(String(255))
   userfullname = Column(String(255))
   useremailaddress = Column(String(255))
   passwordsalt = Column(String(255))
   passwordhash = Column(String(255))

   roles = relation("RoleMember")

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
      rolemember = RoleMember( role )
      self.roles.append(rolemember)

class AI(Base):
   __tablename__ = 'ais'

   ai_id = Column(Integer,primary_key=True)
   ai_name = Column(String(255))
   ai_version = Column(String(255))
   ai_downloadurl = Column(String(255))
   ai_owneraccount_id = Column(Integer,ForeignKey('accounts.account_id'))

   allowedmaps = relation("AIAllowedMap")
   allowedmods = relation("AIAllowedMod")
   allowedoptions = relation("AIAllowedOption")

   owneraccount = relation("Account")

   def __init__( self, ai_name, ai_version ):
      self.ai_name = ai_name
      self.ai_version = ai_version

class AIAllowedMap(Base):
   __tablename__ = 'ai_allowedmaps'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   map_id = Column(Integer,ForeignKey('maps.map_id'),primary_key=True)

   ai = relation("AI")
   map = relation("Map")

class AIAllowedMod(Base):
   __tablename__ = 'ai_allowedmods'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   mod_id = Column(Integer,ForeignKey('mods.mod_id'),primary_key=True)

   ai = relation("AI")
   mod = relation("Mod")

class AIAllowedOption(Base):
   __tablename__ = 'ai_allowedoptions'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   ai = relation("AI")
   option = relation("AIOption")

   def __init__ ( self, option ):
      self.option = option

class Cookie(Base):
   __tablename__ = 'cookies'

   def __init__( self, cookiereference, account ):
      self.cookiereference = cookiereference
      self.account = account

   cookiereference = Column(String(255),primary_key=True)
   #username = Column(String(255))
   # we can change to use account_id in the future
   account_id = Column(Integer,ForeignKey('accounts.account_id'))

   account = relation("Account")

# I think this was in transition when I switched to doing something else ;-)
#class BotRunnerOption(Base):
#   __tablename__ = 'botrunner_options'
#
#   botrunner_option_id = Column(Integer,primary_key=True)
#   botrunner_option_name = Column(String(255))

class BotRunnerSupportedMap(Base):
   __tablename__ = 'botrunner_supportedmaps'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   map_id = Column(Integer,ForeignKey('maps.map_id'),primary_key=True)

   map = relation("Map",uselist = False)

   def __init__(self, map ):
      self.map = map

class BotRunnerSupportedAI(Base):
   __tablename__ = 'botrunner_supportedais'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'), primary_key = True)
   ai_id = Column(Integer,ForeignKey('ais.ai_id'), primary_key = True )

   ai = relation("AI")

   def __init__ (self, ai ):
      self.ai = ai

class BotRunnerSupportedMod(Base):
   __tablename__ = 'botrunner_supportedmods'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   mod_id = Column(Integer,ForeignKey('mods.mod_id'),primary_key=True)

   mod = relation("Mod")

   def __init__(self, mod ):
      self.mod = mod

class BotRunnerAssignedOption(Base):
   __tablename__ = 'botrunner_assignedoptions'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   botrunner_option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   option = relation("AIOption")

   def __init__(self, option ):
      self.option = option

class BotRunnerSession(Base):
   __tablename__ = 'botrunner_sessions'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'), primary_key = True )
   botrunner_session_id = Column(String(255), primary_key = True)
   lastpingstatus = Column(String(255))
   lastpingtime = Column(String(255))

   def __init__(self, botrunner_session_id ):
      self.botrunner_session_id = botrunner_session_id

      self.pingtimeok = False # used by viewbotrunners.py
      self.lastpingtimestring = '' # used by viewbotrunners.py

class BotRunner(Base):
   __tablename__ = 'botrunners'

   botrunner_id = Column(Integer,primary_key=True)
   botrunner_name = Column(String(255))
   botrunner_sharedsecret = Column(String(255))
   botrunner_owneraccountid = Column(Integer, ForeignKey('accounts.account_id') )
   rowspan = 0 # used by viewbotrunners.py

   owneraccount = relation("Account")
   options = relation("BotRunnerAssignedOption")
   supportedmaps = relation("BotRunnerSupportedMap", uselist=True )
   supportedmods = relation("BotRunnerSupportedMod", uselist=True )
   supportedais = relation("BotRunnerSupportedAI", uselist = True )
   sessions = relation("BotRunnerSession",uselist = True)

   rowspan = 0

   def __init__( self, botrunner_name, botrunner_sharedsecret ):
      self.botrunner_name = botrunner_name
      self.botrunner_sharedsecret = botrunner_sharedsecret

class AIOption(Base):
   __tablename__ = 'aioptions'

   option_id = Column(Integer,primary_key=True)
   option_name = Column(String(255))

   def __init__(self, option_name):
      self.option_name = option_name

class MatchRequestOption(Base):
   __tablename__ = 'matchrequest_options'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'), primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   option = relation("AIOption")

   def __init__(self, option ):
      self.option = option

class MatchRequest(Base):
   __tablename__ = 'matchrequestqueue'

   matchrequest_id=Column(Integer,primary_key=True)
   map_id =Column(Integer, ForeignKey('maps.map_id'))
   mod_id =Column(Integer, ForeignKey('mods.mod_id'))
   ai0_id = Column(Integer, ForeignKey('ais.ai_id'))
   ai1_id = Column(Integer, ForeignKey('ais.ai_id'))
   league_id = Column( Integer, ForeignKey('leagues.league_id'))

   map = relation("Map" )
   mod = relation("Mod" )
   ai0 = relation("AI", primaryjoin = ai0_id == AI.ai_id )
   ai1 = relation("AI", primaryjoin = ai1_id == AI.ai_id )

   matchrequestinprogress = relation("MatchRequestInProgress", uselist=False)
   matchresult = relation("MatchResult", uselist=False)
   options = relation("MatchRequestOption")
   league = relation("League", uselist=False)

   def __init__( self, ai0, ai1, map, mod, league = None ):
      self.ai0 = ai0
      self.ai1 = ai1
      self.map = map
      self.mod = mod
      self.league = league

class MatchRequestInProgress(Base):
   __tablename__ = 'matchrequests_inprogress'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),ForeignKey('botrunner_sessions.botrunner_id'))
   botrunner_session_id = Column(String(255),ForeignKey('botrunner_sessions.botrunner_session_id'))
   datetimeassigned = Column(String(255))

   botrunner= relation("BotRunner")
   botrunnersession = relation("BotRunnerSession", primaryjoin=and_( botrunner_id == BotRunnerSession.botrunner_id, botrunner_session_id == BotRunnerSession.botrunner_session_id ) )

   def __init__(self, botrunner, botrunnersession, datetimeassigned ):
      self.botrunner = botrunner
      self.botrunnersession = botrunnersession
      self.datetimeassigned = datetimeassigned

class MatchResult(Base):
   __tablename__ = 'matchresults'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   matchresult = Column(String(255))

   def __init__(self, matchresult ):
      self.matchresult = matchresult

class League(Base):
   __tablename__ = 'leagues'

   league_id = Column(Integer,primary_key = True )
   league_name = Column(String(255))
   league_creatorid = Column(Integer,ForeignKey('accounts.account_id'))
   map_id = Column(Integer,ForeignKey('maps.map_id'))
   mod_id = Column(Integer,ForeignKey('mods.mod_id'))
   nummatchesperaipair = Column(Integer)

   creator = relation("Account")
   map = relation("Map")
   mod = relation("Mod")
   options = relation("LeagueOption")

   def __init__( self, league_name, creator, mod, map, nummatchesperaipair ):
      self.league_name = league_name
      self.creator = creator
      self.mod = mod
      self.map = map
      self.nummatchesperaipair = nummatchesperaipair

class LeagueOption(Base):
   __tablename__ = 'leagueoptions'

   league_id = Column(Integer,ForeignKey('leagues.league_id'),primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   option = relation("AIOption")

   def __init__(self, option ):
      self.option = option

class LeagueGroup(Base):
   __tablename__ = 'leaguegroups'

   leaguegroup_id = Column(Integer,primary_key = True)
   leaguegroup_name = Column(String(255))
   leaguegroup_creatorid = Column(Integer,ForeignKey("accounts.account_id"))
   
   creator = relation("Account")
   childleagues = relation("LeagueGroupLeagueMember")
   #childleaguegroups = relation("LeagueGroupLeagueGroupMember")

   def __init__( self, leaguegroup_name ):
      self.leaguegroup_name = leaguegroup_name

# members who are leaguegruops
class LeagueGroupLeagueMember(Base):
   __tablename__ = 'leaguegroup_leaguemembers'

   leaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key = True)
   league_id = Column(Integer,ForeignKey('leagues.league_id'),primary_key = True)

   league = relation("League")

   def __init__(self, league ):
      self.league = league

# members who are leagues (leaf nodes)
def LeagueGroupLeagueGroupMember(Base):
   __tablename__ = 'leaguegroup_leaguegroupmembers'

   leaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key = True)
   childleaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key=True)

   parentleaguegroup = relation("LeagueGroup", primaryjoin = leaguegroup_id == LeagueGroup.leaguegroup_id, backrefs = 'childleaguegroups')
   leaguegroup = relation("LeagueGroup", primaryjoin = childleaguegroup_id == LeagueGroup.leaguegroup_id)

   def __init__(self, leaguegroup ):
      self.leaguegroup = leaguegroup

# simple flat config for now
class Config(Base):
   __tablename__ = 'config'

   config_key = Column(String(255),primary_key = True )
   config_value = Column(String(255))
   config_type = Column(String(255))

   # sets value of config_type appropriately, according to config_value type
   # to int, float, string or boolean
   def __init__(self, config_key, config_value ):
      self.config_key = config_key
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
   session.add(Config('gametimeoutminutes', 30 ) )
   session.add(Config('expiresessionminutes', 20 ) )
   session.add(Config('gameendstring', "] Team%TEAMNUMBER%" ) )
   session.add(Config('cheatingstring', "] SkirmishAI (with team ID = %TEAMNUMBER%): Cheating enabled" ) )

   # maybe roles static data could be created by core/roles.py?
   # anyway, for now... :
   accountadminrole = Role("accountadmin")
   aiadminrole = Role("aiadmin")
   modadminrole = Role("modadmin")
   mapadminrole = Role("mapadmin")
   leagueadminrole = Role("leagueadmin")
   botrunneradminrole = Role("botrunneradmin")

   session.add(accountadminrole)
   session.add(aiadminrole)
   session.add(modadminrole)
   session.add(mapadminrole)
   session.add(leagueadminrole)
   session.add(botrunneradminrole)

   account = Account("admin","admin", "admin")
   session.add(account)
   account.addRole( accountadminrole )
   account.addRole( aiadminrole )
   account.addRole( modadminrole )
   account.addRole( mapadminrole )
   account.addRole( leagueadminrole )
   account.addRole( botrunneradminrole )

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



