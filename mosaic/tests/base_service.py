#!/usr/bin/env python3.5

import unittest
from mosaic import base_service
from mosaic import exceptions


class TestBaseService(unittest.TestCase):
    def setUp(self):
        self.test_params_default = {
            'ip': '127.0.0.1',
            'port': 5001,
            'name': 'anonymous-service'
        }

        self.test_params_1 = {
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service'
        }

        self.test_params_2 = {
            'port': 7677,
            'name': 'missing-param-service'
        }

    def test_init(self):
        # test initiatiaton without parameters
        self.assertRaises(exceptions.ParameterMissingException, base_service.BaseService, None)

        # test initiation with at least 1 param missing
        self.assertRaises(exceptions.ParameterMissingException, base_service.BaseService, {
            'ip': '127.0.0.1',
            'name': 'fancy-service'
        })

        self.assertRaises(exceptions.ParameterMissingException, base_service.BaseService, {
            'ip': '127.0.0.1'
        })

        # test initiation with params
        bs_with_params = base_service.BaseService({
            'ip': '127.0.0.1',
            'port': 6867,
            'name': 'fancy-service'
        })
        self.assertDictEqual(bs_with_params.params, self.test_params_1)

        # test initiation with a missing parameter
        # TODO test missing parameters (start child process and test output)

if __name__ == '__main__':
    unittest.main()
