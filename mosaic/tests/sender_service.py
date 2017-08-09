#!/usr/bin/env python3.5

import unittest

from mosaic.tests.classes import sender_service


class TestNumberService(unittest.TestCase):
    def setUp(self):
        self.number_service = sender_service.SenderService()


if __name__ == '__main__':
    unittest.main()
