import unittest
import re
import time
import os
from os.path import join
from tempfile import TemporaryDirectory
from mosaic.monitor import basic_monitoring
from mosaic import exceptions


class TestLogging(unittest.TestCase):
 
    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_basic_monitoring(self):
        self.assertRaises(exceptions.ParameterMissing, basic_monitoring.BasicMonitoring)

if __name__ == '__main__':
    unittest.main()
