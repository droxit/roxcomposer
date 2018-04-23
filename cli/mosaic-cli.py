#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# mosaic-cli.py
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

from functools import partial
from urwid import *
from commands import cmd_map, list_commands, run_cmd
from cmdparser import tokenize


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
        self.cmd_walk = 0
        self.watchers = []
        self.loop = None
        body = Pile([self.log, self.cmdh])
        super(MainFrame, self).__init__(body, footer=self.cmdl)

    def store_loop(self, loop):
        self.loop = loop

    def call_and_refresh(self, loop, data):
        callback, refresh_interval = data
        try:
            ret = callback()
            if len(ret):
                self.log.addline(ret)
            self.loop.set_alarm_in(refresh_interval, self.call_and_refresh, (callback, refresh_interval))
        except Exception as e:
            self.log.addline("Watcher terminated: {}".format(e))

    def add_watcher(self, callback, refresh_interval):
        if self.loop is not None:
            self.loop.set_alarm_in(refresh_interval, self.call_and_refresh, (callback, refresh_interval))

    def keypress(self, size, key):
        if self.focus_position == 'footer':
            if key == 'up' or key == 'down':
                if key == 'up':
                    self.cmd_walk += 1
                if key == 'down':
                    self.cmd_walk -= 1
                self.cmd_walk = min(max(self.cmd_walk, 0), len(self.cmdh.body))
                if self.cmd_walk > 0:
                    line = len(self.cmdh.body) - self.cmd_walk
                    self.cmdl.set_text(self.cmdh.body[line].get_text()[0])
                else:
                    self.cmdl.set_text(u"")

        if key != 'enter':
            return super(MainFrame, self).keypress(size, key)

        self.cmd_walk = 0
        cmd = self.cmdl.get_text()

        # do not react on empty input
        if cmd == "":
            return super(MainFrame, self).keypress(size, key)

        # stop on exit
        if cmd == "exit":
            raise ExitMainLoop()

        cmdt = tokenize(cmd)

        # command not available
        if cmdt[0] not in cmd_map:
            self.log.addline(list_commands())
        else:
            ret = run_cmd(*cmdt)
            if isinstance(ret, str):
                self.log.addline(ret)
            elif isinstance(ret, dict):
                self.log.addline(ret['response'])
                if 'callback' in ret:
                    self.add_watcher(ret['callback'], 0.2)

        self.cmdh.addline(cmd)
        self.cmdl.clear()


class CommandLine(LineBox):
    def __init__(self):
        self.edit = Edit(u"")
        super(CommandLine, self).__init__(self.edit)

    def get_text(self):
        return self.edit.edit_text

    def set_text(self, txt):
        self.edit.edit_text = txt

    def clear(self):
        self.edit.edit_text = u""


if __name__ == "__main__":
    frame = MainFrame()
    frame.focus_position = 'footer'
    loop = MainLoop(frame)
    frame.store_loop(loop)
    loop.run()
