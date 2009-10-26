#!/usr/bin/python


from core import *

sqlalchemysetup.setup()

jinjahelper.rendertemplate("architecture.html")

sqlalchemysetup.close()


