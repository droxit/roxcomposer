#!/usr/bin/env python3.5

import unittest

from mosaic.tests.classes import html_generator


class TestNumberService(unittest.TestCase):
    def setUp(self):
        self.number_service = html_generator.HtmlGenerator()


if __name__ == '__main__':
    unittest.main()
