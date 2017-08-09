#!/usr/bin/env python3.5

import unittest
from mosaic import base_service


class TestBaseService(unittest.TestCase):
    def setUp(self):
        self.init_base_service = base_service.BaseService()

    def test_init(self):
        self.assertTrue(self.init_base_service.get_mosaic_message().HasField('pipeline'))

if __name__ == '__main__':
    unittest.main()
