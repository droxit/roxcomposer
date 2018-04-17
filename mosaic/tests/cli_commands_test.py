# encoding: utf-8
#
# Tests for the cli commands
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#

import unittest
import json
from cli import commands
import mosaic.tests.classes.dummy_connector as dummy_connector


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.server = dummy_connector.DummyConnector()
        self.server.start()

    def test_load_services_and_pipeline(self):
        response ='{"checkin":{"services":["html_generator","file_writer"],"active":true}}'
        args = {
                "services": {
                    "html_generator": {
                        "classpath": "mosaic.tests.classes.html_generator.HtmlGenerator",
                        "params": {
                            "ip": "127.0.0.1",
                            "name": "html_generator",
                            "port": 5002
                        }
                    },
                    "file_writer": {
                        "classpath": "mosaic.tests.classes.file_writer.FileWriter",
                        "params": {
                            "ip": "127.0.0.1",
                            "name": "file_writer",
                            "filepath": "mosaic_demo.html",
                            "port": 5001
                        }
                    }
                },
                "pipelines": {
                    "checkin": {
                        "services": ["html_generator", "file_writer"]
                    }
                }
        }

        commands.load_services_and_pipelines(*[json.dumps(args)])
        request = commands.get_pipelines(*[])
        self.assertEqual(response, request)

    def tearDown(self):
        self.server.stop()



if __name__ == '__main__':
    unittest.main()