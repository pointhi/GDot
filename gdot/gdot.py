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

import os
import argparse

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, GtkSource, GObject  # noqa

gi.require_version('PangoCairo', '1.0')
from xdot import DotWidget # noqa

# register "non standard" widgets which we require
GObject.type_register(GtkSource.View)


class GDot(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.builder.add_from_file(os.path.join(script_dir, "gdot.glade"))
        self.builder.connect_signals(self)

        self.header_bar = self.builder.get_object("header_bar")

        self.code_editor = self.builder.get_object("source_code")
        self.code_buffer = self.code_editor.get_buffer()
        self.lm = GtkSource.LanguageManager.new()
        self.code_buffer.set_language(self.lm.get_language("dot"))

        self.dotwidget = DotWidget()
        diagram_container = self.builder.get_object("diagram_container")
        diagram_container.pack_start(self.dotwidget, True, True, 0)

        self.open_file_chooser = self.builder.get_object("btn_file_chooser")
        self._set_dotfile_filter(self.open_file_chooser)

        self.set_working_dir(os.getcwd())

        self.window = self.builder.get_object("application")
        self.window.show_all()

    @staticmethod
    def _set_dotfile_filter(file_chooser):
        filter_dot = Gtk.FileFilter()
        filter_dot.set_name("Graphviz dot files")
        filter_dot.add_pattern("*.dot")
        file_chooser.add_filter(filter_dot)

        filter_all = Gtk.FileFilter()
        filter_all.set_name("All files")
        filter_all.add_pattern("*")
        file_chooser.add_filter(filter_all)

    @staticmethod
    def on_delete_window(*args):
        Gtk.main_quit(*args)

    def on_load_new_file(self, chooser):
        filename = chooser.get_filename();
        folder = chooser.get_current_folder()
        self.open_file(filename)
        if folder:
            self.set_working_dir(folder)

    def on_btn_save_as(self, button):
        self.save_as_file()

    def on_btn_reload(self, button):
        self.update_dotwidget()

    def on_btn_export(self, button):
        print('export')

    def on_btn_zoom_in(self, button):
        self.dotwidget.on_zoom_in(button)

    def on_btn_zoom_out(self, button):
        self.dotwidget.on_zoom_out(button)

    def on_btn_zoom_fit(self, button):
        self.dotwidget.on_zoom_fit(button)

    def on_btn_zoom_100(self, button):
        self.dotwidget.on_zoom_100(button)

    def open_file(self, path):
        with open(path, 'r') as fp:
            self.set_dotcode(fp.read())
            self.header_bar.set_subtitle(path)

            self.open_file_chooser.set_filename(path)

    def save_as_file(self):
        chooser = Gtk.FileChooserDialog(parent=self.window,
                                        title="Save dot File",
                                        action=Gtk.FileChooserAction.SAVE,
                                        buttons=(Gtk.STOCK_CANCEL,
                                                 Gtk.ResponseType.CANCEL,
                                                 Gtk.STOCK_SAVE ,
                                                 Gtk.ResponseType.OK))
        chooser.set_default_response(Gtk.ResponseType.OK)
        old_filename = self.open_file_chooser.get_filename()
        if old_filename:
            chooser.set_filename(old_filename)
        self._set_dotfile_filter(chooser)

        if chooser.run() == Gtk.ResponseType.OK:
            filename = chooser.get_filename()
            folder = chooser.get_current_folder()
            chooser.destroy()

            if not os.path.splitext(filename)[1]:
                filename = '{}.dot'.format(filename)

            # TODO: file already exists dialog

            self.save_file(filename)

            self.open_file_chooser.set_filename(filename)
            self.set_working_dir(folder)
            return True
        else:
            chooser.destroy()
            return False

    def save_file(self, path):
        with open(path, 'w') as fp:
            fp.write(self.get_dotcode())
            self.header_bar.set_subtitle(path)

    def get_dotcode(self):
        start_iter = self.code_buffer.get_start_iter()
        end_iter = self.code_buffer.get_end_iter()
        return self.code_buffer.get_text(start_iter, end_iter, True)

    def set_dotcode(self, dotcode):
        self.code_buffer.begin_not_undoable_action()
        self.code_buffer.set_text(dotcode)
        self.code_buffer.end_not_undoable_action()

        self.update_dotwidget()

    def set_working_dir(self, dir):
        self.open_file_chooser.set_current_folder(dir)
        os.chdir(dir)

    def update_dotwidget(self):
        self.dotwidget.set_dotcode(self.get_dotcode(), None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GUI to edit and view graphviz files')
    parser.add_argument('dotfile', nargs='?', type=str)

    args = parser.parse_args()

    # load our main application
    gdot = GDot()

    # load file if specified
    if args.dotfile:
        gdot.open_file(args.dotfile)

    # workaround to support KeyboardInterrupt
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # startup gui
    Gtk.main()
