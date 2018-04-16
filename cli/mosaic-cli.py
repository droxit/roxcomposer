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
from commands import cmd_map, run_cmd
from cmdparser import tokenize
import json


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


class ProgressWindow(LineBox):
    def __init__(self, caption, done):
        self.pbar = ProgressBar('normal', 'complete', done=done)
        self.body = SimpleFocusListWalker([])
        super(ProgressWindow, self).__init__(Frame(ListBox(self.body), header=self.pbar), title=caption)

    def fill(self, content):
        self.body.clear()
        lines = content.split("\n")
        for line in lines:
            self.body.append(Text(line.strip()))
            self.body.set_focus(len(self.body) - 1)

    def progress(self, completion):
        self.pbar.set_completion(completion)


class MainFrame(Frame):
    def __init__(self):
        self.log = Window(u"Log Window")
        self.mtw = MessageTraceWidget(self)
        self.cmdh = Window(u"Command History")
        self.cmdl = CommandLine()
        self.cmd_walk = 0
        self.body = Pile([])
        self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 0)), (self.cmdh, (WEIGHT, 1))]
        super(MainFrame, self).__init__(self.body, footer=self.cmdl)

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
            self.log.addline(run_cmd(*['help']))
        elif cmdt[0] == "post_to_pipeline":
            try:
                msg_id = run_cmd(*cmdt)
                pipelines = run_cmd(*['pipelines'])
                pipe_len = len(json.loads(pipelines)[cmdt[1]]['services'])
                self.mtw.add_message(msg_id, pipe_len)
            except Exception as e:
                self.log.addline(str(e))
        else:
            self.log.addline(run_cmd(*cmdt))

        self.cmdh.addline(cmd)
        self.cmdl.clear()

    def showmtw(self, show):
        if show:
            self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 1)), (self.cmdh, (WEIGHT, 1))]
        else:
            self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 0)), (self.cmdh, (WEIGHT, 1))]


class MessageTraceWidget(Pile):
    def __init__(self, parent):
        self.message_map = dict()
        self.pipe_lens = dict()
        self.parent = parent
        super(MessageTraceWidget, self).__init__([])

    def add_message(self, msg_id, pipe_len):
        if msg_id in self.message_map.keys():
            self.parent.log.addline("Message tracing failed: ID duplicate.")
            return
        self.message_map[msg_id] = ProgressWindow(u"Message "+str(msg_id), pipe_len)
        self.pipe_lens[msg_id] = pipe_len
        self.parent.showmtw(True)
        self.parent.log.addline("Message tracing started: "+msg_id)

    def remove_message(self, msg_id):
        if msg_id not in self.message_map.keys():
            self.parent.log.addline("Message tracing stop failed: ID not found.")
            return
        del self.message_map[msg_id]
        if not self.message_map:
            self.parent.showmtw(False)
        self.parent.log.addline("Message tracing finished: "+msg_id)

    def refresh(self, loop=None, data=None):
        # do update with collecting the finished
        finished = []
        for key in self.message_map.keys():
            msg_hist = json.loads(run_cmd(*['get_msg_history', key]))
            msg_hist = "\n".join([json.dumps(msg) for msg in msg_hist])

            sub = '"event": "message_dispatched"'
            completion = msg_hist.count(sub)
            if '"event": "message_final_destination"' in msg_hist:
                completion += 1
                finished.append(key)
            self.message_map[key].progress(completion)
            self.message_map[key].fill(msg_hist)

        # remove finished
        for key in finished:
            self.remove_message(key)

        self.contents = [(w, (WEIGHT, 1)) for w in self.message_map.values()]
        loop.set_alarm_in(1, self.refresh)


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

    palette = [
        ('normal',   'white', 'black', 'standout'),
        ('complete', 'white', 'dark magenta'),
    ]

    loop = MainLoop(frame, palette)
    loop.set_alarm_in(1, frame.mtw.refresh)
    loop.run()
