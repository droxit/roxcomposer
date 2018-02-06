# encoding: utf-8
#
# monitor testing class - for testing purposes only
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#


from mosaic.base_service import BaseService


class MonitorTest(BaseService):
    def __init__(self, params):
        super().__init__(params)

    def do_receive(self):
        self.monitoring.msg_received()

    def do_dispatch(self):
        self.monitoring.msg_dispatched()

    def do_destination(self):
        self.monitoring.msg_reached_final_destination()

    def do_error(self):
        self.monitoring.msg_error()
