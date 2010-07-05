#
# gtkui.py
#
# Copyright (C) 2008 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#
#

import gtk

from deluge.log import LOG as log
from deluge.ui.client import client
from deluge.plugins.pluginbase import GtkPluginBase
import deluge.component as component
import deluge.common
import deluge.configmanager

from common import get_resource

class GtkUI(GtkPluginBase):
    def enable(self):
    
        self.glade = gtk.glade.XML(get_resource("config.glade"))
        
        component.get("PluginManager").register_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").register_hook("on_show_prefs", self.on_show_prefs)
        component.get("Preferences").add_page("Growl", self.glade.get_widget("prefs_box"))
        
    def disable(self):
        component.get("Preferences").remove_page("Growl")
        component.get("PluginManager").deregister_hook("on_apply_prefs", self.on_apply_prefs)
        component.get("PluginManager").deregister_hook("on_show_prefs", self.on_show_prefs)

    def on_show_prefs(self):
        client.growl.get_config().addCallback(self.cb_get_config)

    def cb_get_config(self, core_config):
        self.glade.get_widget("growl_sticky").set_active(core_config["growl_sticky"])
        self.glade.get_widget("growl_torrent_added").set_active(core_config["growl_torrent_added"])
        self.glade.get_widget("growl_torrent_completed").set_active(core_config["growl_torrent_completed"])
        self.glade.get_widget("growl_host").set_text(core_config["growl_host"])
        self.glade.get_widget("growl_port").set_value(core_config["growl_port"])
        self.glade.get_widget("growl_password").set_text(core_config["growl_password"])
        self.glade.get_widget("growl_priority").set_active(core_config["growl_priority"]+2)
            
    def on_apply_prefs(self):
        core_config = {
            "growl_sticky": self.glade.get_widget("growl_sticky").get_active(),
            "growl_torrent_added": self.glade.get_widget("growl_torrent_added").get_active(),
            "growl_torrent_completed": self.glade.get_widget("growl_torrent_completed").get_active(),
            "growl_host": self.glade.get_widget("growl_host").get_text(),
            "growl_port": self.glade.get_widget("growl_port").get_value(),
            "growl_password": self.glade.get_widget("growl_password").get_text(),
            "growl_priority": self.glade.get_widget("growl_priority").get_active()-2
        }

        client.growl.set_config(core_config)
        #client.growl.get_config().addCallback(self.cb_get_config)
