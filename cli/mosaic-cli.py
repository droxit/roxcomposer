#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mosaic-cli.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

from urwid import *
from commands import cmd_map, list_commands


class Window(LineBox):
    def __init__(self, caption):
        self.body = SimpleFocusListWalker([])
        super(Window, self).__init__(ListBox(self.body), title=caption)

    def addline(self, line):
        self.body.append(Text(line))
        self.body.set_focus(len(self.body)-1)

    def fill(self, content):
        self.body.clear()
        lines = content.split("\n")
        for line in lines:
            self.body.append(Text(line.strip()))
            self.body.set_focus(len(self.body) - 1)


class MainFrame(Frame):
    def __init__(self):
        self.log = Window(u"Log Window")
        self.cmdh = Window(u"Command History")
        self.cmdl = CommandLine()
        body = Pile([self.log, self.cmdh])
        super(MainFrame, self).__init__(body, footer=self.cmdl)

    def keypress(self, size, key):
        if key != 'enter':
            return super(MainFrame, self).keypress(size, key)
        cmd = self.cmdl.get_text()

        # stop on exit
        if cmd == "exit":
            raise ExitMainLoop()

        # command not available
        if cmd not in cmd_map:
            self.log.fill(list_commands()+"\n exit")

        self.cmdh.addline(cmd)
        self.cmdl.clear()


class CommandLine(LineBox):
    def __init__(self):
        self.edit = Edit(u"")
        super(CommandLine, self).__init__(self.edit)

    def get_text(self):
        return self.edit.edit_text

    def clear(self):
        self.edit.edit_text = u""


if __name__ == "__main__":
    frame = MainFrame()
    frame.focus_position = 'footer'
    loop = MainLoop(frame)
    loop.run()
