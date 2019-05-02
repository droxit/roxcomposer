# encoding: utf-8
#
# Tests for the cli commands
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#

import unittest
import json
from os.path import join
from cli import commands
from tempfile import TemporaryDirectory
import roxcomposer.tests.classes.dummy_connector as dummy_connector


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.server = dummy_connector.DummyConnector()
        self.server.start()
        self.maxDiff = None

    def test_msg_history(self):
        command = '{"message_id": "msg_id"}'
        sent = commands.get_msg_history(*['msg_id'])
        self.assertEqual(command, sent)

        err = "WARNING: superfluous arguments to get msg history: ('msg_id', 'other stuff')"
        sent2 = commands.get_msg_history(*['msg_id', 'other stuff'])
        self.assertEqual(err, sent2)

    def test_post_to_pipeline(self):
        command = {"name": "pipe", "data": "Hello World"}
        sent = commands.post_to_pipeline(*['pipe', 'Hello', 'World'])
        self.assertDictEqual(command, json.loads(sent))

        with self.assertRaises(RuntimeError):
            commands.post_to_pipeline(*['pipe'])

    def test_watch_services(self):
        ret = commands.watch_services()
        self.assertRegex(ret, "ERROR")
        commands.watch_services("s1", "s2")
        ret = commands.watch_services("s1")
        self.assertEqual(ret, "All services already watched")
        commands.unwatch_services("s1", "s2")
        ret = commands.watch_services("s1")
        self.assertNotEqual(ret, "All services already watched")

    def test_watch_pipelines(self):
        ret = commands.watch_pipelines()
        self.assertRegex(ret, "ERROR")
        ret = commands.watch_pipelines("notapipe")
        self.assertRegex(ret, "ERROR")
        ret = commands.watch_pipelines("pipe")
        self.assertNotEqual(ret, "All services already watched")
        ret = commands.watch_pipelines("pipe")
        self.assertEqual(ret, "All services already watched")
        commands.unwatch_pipelines("pipe")
        
    def test_load_services_and_pipeline(self):
        resp = {"pipelines": {"composer_test": {"services": ["html_generator", "file_writer"]}}, "services": {"file_writer": {"params": {"ip": "127.0.0.1", "name": "file_writer", "filepath": "roxcomposer_demo.html", "port": 5001}, "classpath": "roxcomposer.tests.classes.file_writer.FileWriter"}, "html_generator": {"params": {"ip": "127.0.0.1", "name": "html_generator", "port": 5002}, "classpath": "roxcomposer.tests.classes.html_generator.HtmlGenerator"}}}
        args = {
                'services': {
                    'html_generator': {
                        'classpath': 'roxcomposer.tests.classes.html_generator.HtmlGenerator',
                        'params': {
                            'ip': '127.0.0.1',
                            'name': 'html_generator',
                            'port': 5002
                        }
                    },
                    'file_writer': {
                        'classpath': 'roxcomposer.tests.classes.file_writer.FileWriter',
                        'params': {
                            'ip': '127.0.0.1',
                            'name': 'file_writer',
                            'filepath': 'roxcomposer_demo.html',
                            'port': 5001
                        }
                    }
                },
                'pipelines': {
                    'composer_test': {
                        'services': ['html_generator', 'file_writer']
                    }
                }
        }

        with TemporaryDirectory() as tdir:
            dummy_path = join(tdir, 'dummy_test.log')

            f = open(dummy_path, "w")
            f.write(json.dumps(args))
            f.close()

            sent = commands.load_services_and_pipelines(*[dummy_path])
            self.maxDiff = None
            self.assertDictEqual(resp, json.loads(sent))

    def test_set_pipeline(self):
        pipename = 'dummy_test'
        services = ['html_generator']
        sent = commands.set_pipeline(pipename, services)

        response = {"services": [["html_generator"]], "name": "dummy_test",}
        self.assertDictEqual(response, json.loads(sent))

    def test_shutdown_service(self):
        service = 'html_generator'
        sent = commands.shutdown_service(service)
        response = {"name": "html_generator"}

        self.assertEqual(response, json.loads(sent))

    def test_shutdown_service_false(self):
        sent = commands.shutdown_service()
        response = 'ERROR: exactly one service needs to be specified for shutdown'

        self.assertEqual(response, sent)

    def test_services(self):
        sent = commands.get_services('blabla')
        response = 'WARNING: superfluous arguments to services: (\'blabla\',)'

        self.assertEqual(response, sent)

    def test_pipelines(self):
        sent = commands.get_pipelines('blabla')
        response = '{"pipe": {"services": ["s1", "s2"], "active": true}}'
        self.assertEqual(response, sent)

    def tearDown(self):
        self.server.stop()

class TestCliCommandsDisconnected(unittest.TestCase):

    def test_msg_history_disconnected(self):
        command = '{"message_id": "msg_id"}'
        ret = commands.get_msg_history(*['msg_id'])
        self.assertIn("ERROR: no connection to server", ret)

    def test_post_to_pipeline_disconnected(self):
        command = '{"name": "pipe", "data": "Hello World"}'
        ret = commands.post_to_pipeline(*['pipe', 'Hello', 'World'])
        self.assertIn("ERROR: no connection to server", ret)

    def test_watch_services_disconnected(self):
        ret = commands.watch_services("bla", "blub")
        self.assertIn("ERROR: no connection to server", ret)

if __name__ == '__main__':
    unittest.main()

