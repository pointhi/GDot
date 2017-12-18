#!/usr/bin/env python3

'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

(C) 2017 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>
'''


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, GtkSource, GObject  # noqa

# register "non standard" widgets which we require
GObject.type_register(GtkSource.View)


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)


if __name__ == '__main__':
    builder = Gtk.Builder()
    builder.add_from_file("ui/gdot.glade")
    builder.connect_signals(Handler())

    window = builder.get_object("application")
    window.show_all()

    # workaround to support KeyboardInterrupt
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # startup gui
    Gtk.main()
