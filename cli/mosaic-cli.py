#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Urwid based CLI application for ROXcomposer
# It can be used to start and shutdown services, setup pipelines and post messages.
# Once a message is posted, it will be traced back automatically by using the message history.
#
# devs@droxit.de - droxIT GmbH
#
# Copyright (c) 2018 droxIT GmbH
#

from functools import partial
from urwid import *
from commands import cmd_map, run_cmd
from cmdparser import tokenize
import json


# Window class - for boxed windows with listed elements
class Window(LineBox):
    def __init__(self, caption):
        self.body = SimpleFocusListWalker([])
        super(Window, self).__init__(ListBox(self.body), title=caption)

    # add a singe text line to the window
    def addline(self, line):
        self.body.append(Text(line))
        self.body.set_focus(len(self.body)-1)

    # overwrite the window content
    def fill(self, content):
        self.body.clear()
        lines = content.split("\n")
        for line in lines:
            self.body.append(Text(line.strip()))
            self.body.set_focus(len(self.body) - 1)


# ProgressWindow class - for boxed windows with listed elements and progress bar header
class ProgressWindow(LineBox):
    def __init__(self, caption, done):
        self.pbar = ProgressBar('normal', 'complete', done=done)
        self.body = SimpleFocusListWalker([])
        super(ProgressWindow, self).__init__(Frame(ListBox(self.body), header=self.pbar), title=caption)

    # overwrite the window content
    def fill(self, content):
        self.body.clear()
        lines = content.split("\n")
        for line in lines:
            self.body.append(Text(line.strip()))
            self.body.set_focus(len(self.body) - 1)

    # set the current progress for the progress bar
    def progress(self, completion):
        self.pbar.set_completion(completion)


# MainFrame class - main window container and key input handler
class MainFrame(Frame):
    def __init__(self):
        self.log = Window(u"Log Window")
        self.mtw = MessageTraceWidget(self)
        self.cmdh = Window(u"Command History")
        self.cmdl = CommandLine()
        self.cmd_walk = 0
        self.body = Pile([])
        self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 0)), (self.cmdh, (WEIGHT, 1))]
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

    # key input handling function
    def keypress(self, size, key):

        # cmd history walk with up and down arrow keys
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

        # only pass if enter is pressed
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

        # interpret command
        try:
            if cmdt[0] not in cmd_map:
                self.log.addline(run_cmd(('help')))
            elif cmdt[0] == "post_to_pipeline":
                msg_id = json.loads(run_cmd(*cmdt))['message_id']
                pipelines = run_cmd(*['pipelines'])
                pipe_len = len(json.loads(pipelines)[cmdt[1]]['services'])
                self.mtw.add_message(msg_id, pipe_len)
            else:
                ret = run_cmd(*cmdt)
                if isinstance(ret, str):
                    self.log.addline(ret)
                elif isinstance(ret, dict):
                    self.log.addline(ret['response'])
                    if 'callback' in ret:
                        self.add_watcher(ret['callback'], 0.2)
        except Exception as e:
            self.log.addline(str(e))

        self.cmdh.addline(cmd)
        self.cmdl.clear()

    # show and hide message trace window
    def showmtw(self, show):
        if show:
            self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 1)), (self.cmdh, (WEIGHT, 1))]
        else:
            self.body.contents = [(self.log, (WEIGHT, 2)), (self.mtw, (WEIGHT, 0)), (self.cmdh, (WEIGHT, 1))]


# MessageTraceWidget class - message trace windows container
class MessageTraceWidget(Pile):
    def __init__(self, parent):
        self.message_map = dict()
        self.pipe_lens = dict()
        self.parent = parent
        super(MessageTraceWidget, self).__init__([])

    # add a message to the widget.
    # it uses the pipeline length to compute the progress.
    def add_message(self, msg_id, pipe_len):
        if msg_id in self.message_map.keys():
            self.parent.log.addline("Message tracing failed: ID duplicate.")
            return
        self.message_map[msg_id] = ProgressWindow(u"Message "+str(msg_id), pipe_len)
        self.pipe_lens[msg_id] = pipe_len
        self.parent.showmtw(True)
        self.parent.log.addline("Message tracing started: "+msg_id)

    # removes the message from the widget.
    # completed messages are automatically removed during refresh.
    def remove_message(self, msg_id):
        if msg_id not in self.message_map.keys():
            self.parent.log.addline("Message tracing stop failed: ID not found.")
            return
        del self.message_map[msg_id]
        if not self.message_map:
            self.parent.showmtw(False)
        self.parent.log.addline("Message tracing finished: "+msg_id)

    # refreshes the message histories and progress.
    # the progress is computed by the 'message dispatched' event counts and the pipeline length.
    def refresh(self, loop=None, data=None):
        # do update with collecting the finished
        finished = []
        for key in self.message_map.keys():
            msg_hist = []
            try:
                msg_hist = json.loads(run_cmd('get_msg_history', key))
            except Exception as e:
                self.parent.log.addline(str(e))
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
        loop.set_alarm_in(0.1, self.refresh)


# CommandLine class - for boxed edit line used to read the command input
class CommandLine(LineBox):
    def __init__(self):
        self.edit = Edit(u"")
        super(CommandLine, self).__init__(self.edit)

    # read the text from the edit box
    def get_text(self):
        return self.edit.edit_text

    # set a text for the edit box
    def set_text(self, txt):
        self.edit.edit_text = txt

    # clear the edit box
    def clear(self):
        self.edit.edit_text = u""


# Main function
if __name__ == "__main__":
    frame = MainFrame()
    frame.focus_position = 'footer'

    # palette introduces colors with labels 'normal' and 'complete'
    # the colors are used for the progress bars
    palette = [
        ('normal',   'white', 'black', 'standout'),
        ('complete', 'white', 'dark magenta'),
    ]
    loop = MainLoop(frame, palette)
    frame.store_loop(loop)

    # start refreshing loop for the message trace widget
    loop.set_alarm_in(0.1, frame.mtw.refresh)
    loop.run()

