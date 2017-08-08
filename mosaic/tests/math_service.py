#!/usr/bin/env python3.5

import unittest
from mosaic import math_service


class TestMathService(unittest.TestCase):
    def setUp(self):
        self.math_service = math_service.MathService()

    # def test_addition(self):
    #     self.math_service.set_payload(2, 3)
    #     self.assertEqual(self.math_service.addition(), 5)

if __name__ == '__main__':
    unittest.main()
