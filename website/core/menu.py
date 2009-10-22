#!/usr/bin/python

import cgitb; cgitb.enable()
import datetime

import sys
import os

from jinja2 import Environment, PackageLoader

from utils import *
from tableclasses import *

import loginhelper
import jinjahelper

def getmenus():
   menus = []
   if loginhelper.isLoggedOn():
      menus.append([ "Username: " + loginhelper.gusername,[ 
        ['Change Password', 'changepasswordform.py'],
        ['Logout', 'logout.py']
      ]])
   else:
      menus.append(["Login", [
         [ 'Login', 'loginform.py' ]
      ]])
   menus.append(['League', [
      ['View league group results', 'viewleaguegroupresults.py'],
      ['View league results', 'viewleagueresults.py'],
      ['View match results', 'viewresults.py']
   ]])
   menus.append([ 'Runner', [
      ['View request queue', 'viewrequests.py'],
      ['Add request to queue', 'submitrequestform.py'],
      ['View request counts per league', 'showaimatchpaircount.py']
   ]])

   menus.append([ 'Configuration', [
      ['Setup notes', 'setupnotes.py'],
      ['View league groups', 'viewleaguegroups.py'],
      ['View leagues', 'viewleagues.py'],
      ['View available bot runners', 'viewbotrunners.py'],
      ['View available maps', 'viewmaps.py'],
      ['View available mods', 'viewmods.py'],
      ['View available ais', 'viewais.py'],
      ['View accounts', 'viewaccounts.py'],
      ['Run website diagnostics', 'diagnostics.py']
   ]])

   menus.append([ 'About', [
      ['About', 'about.py']
   ]])

   return menus

