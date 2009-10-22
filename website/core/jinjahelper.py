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

import jinja2
import menu

# renders templatename, passing in named args
def rendertemplate( templatename, **args ):
   if not args.has_key('menus'):
      args['menus'] = menu.getmenus()
   env = jinja2.Environment( loader=jinja2.PackageLoader('jinjaapplication', 'templates'))
   template = env.get_template(templatename)
   print template.render( **args )

# displays message in fully laid out page with menus and stuff present
def message( message ):
   rendertemplate( 'genericmessage.html', message = message, menus = menu.getmenus() )

