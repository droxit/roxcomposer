#!/usr/bin/env python3.5

import unittest
from mosaic import number_service


class TestNumberService(unittest.TestCase):
    def setUp(self):
        self.number_service = number_service.NumberService()


if __name__ == '__main__':
    unittest.main()
