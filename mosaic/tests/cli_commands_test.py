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
import os
from os.path import join
from tempfile import TemporaryDirectory
import mosaic.tests.classes.dummy_connector as dummy_connector


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.server = dummy_connector.DummyConnector()
        self.server.start()
        self.maxDiff = None

    def test_load_services_and_pipeline(self):
        resp = {"pipelines": {"composer_test": {"services": ["html_generator", "file_writer"]}}, "services": {"file_writer": {"params": {"ip": "127.0.0.1", "name": "file_writer", "filepath": "mosaic_demo.html", "port": 5001}, "classpath": "mosaic.tests.classes.file_writer.FileWriter"}, "html_generator": {"params": {"ip": "127.0.0.1", "name": "html_generator", "port": 5002}, "classpath": "mosaic.tests.classes.html_generator.HtmlGenerator"}}}
        args = {
                'services': {
                    'html_generator': {
                        'classpath': 'mosaic.tests.classes.html_generator.HtmlGenerator',
                        'params': {
                            'ip': '127.0.0.1',
                            'name': 'html_generator',
                            'port': 5002
                        }
                    },
                    'file_writer': {
                        'classpath': 'mosaic.tests.classes.file_writer.FileWriter',
                        'params': {
                            'ip': '127.0.0.1',
                            'name': 'file_writer',
                            'filepath': 'mosaic_demo.html',
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
            #self.assertEqual(json.dumps(resp), sent)
            self.assertDictEqual(resp, json.loads(sent))

    def test_set_pipeline(self):
        pipename = 'dummy_test'
        services = ['html_generator']
        sent = commands.set_pipeline(pipename, services)

        response = {"name": "dummy_test","services": [["html_generator"]]}
        response2 = {"services": [["html_generator"]], "name": "dummy_test",}
        self.assertEqual(json.dumps(response2), sent)
        self.assertDictEqual(response2, json.loads(sent))

    def test_shutdown_service(self):
        service = 'html_generator'
        sent = commands.shutdown_service(service)
        response = {"name": "html_generator"}

        self.assertEqual(json.dumps(response), sent)

    def test_shutdown_service_false(self):
        sent = commands.shutdown_service()
        response = 'ERROR: exactly one service needs to be specified for shutdown'

        self.assertEqual(response, sent)

    def tearDown(self):
        self.server.stop()



if __name__ == '__main__':
    unittest.main()