#!/usr/bin/env python3

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
