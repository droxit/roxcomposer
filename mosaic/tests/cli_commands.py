# encoding: utf-8
#
# Tests for the cli commands
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import unittest
from cli import commands
import mosaic.tests.classes.connector_dummy as connector_dummy


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.server = connector_dummy.ConnectorDummy()
        self.server.start()

    def test_msg_history(self):
        command = '{"message_id": "msg_id"}'
        sent = commands.get_msg_history(*['msg_id'])
        self.assertEqual(command, sent)

        err = "WARNING: superfluous arguments to get msg history: ('msg_id', 'other stuff')"
        sent2 = commands.get_msg_history(*['msg_id', 'other stuff'])
        self.assertEqual(err, sent2)

    def test_post_to_pipeline(self):
        command = '{"name": "pipe", "data": "Hello World"}'
        sent = commands.post_to_pipeline(*['pipe', 'Hello', 'World'])
        self.assertEqual(command, sent)

        with self.assertRaises(RuntimeError):
            commands.post_to_pipeline(*['pipe'])

    def tearDown(self):
        self.server.stop()


if __name__ == '__main__':
    unittest.main()
