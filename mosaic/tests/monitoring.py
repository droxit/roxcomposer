import unittest
import re
import time
import os
from os.path import join
from tempfile import TemporaryDirectory
from mosaic.monitor import basic_monitoring
from mosaic import exceptions


class TestMonitoring(unittest.TestCase):
 
    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_basic_monitoring(self):
        self.assertRaises(exceptions.ParameterMissing, basic_monitoring.BasicMonitoring)
        self.assertRaises(FileNotFoundError, basic_monitoring.BasicMonitoring, filename='/not/even/remotely/viable')

        with TemporaryDirectory() as tdir:
            fname = 'monitoring_test.log'
            mf = join(tdir, fname)
            mon = basic_monitoring.BasicMonitoring(filename=mf)
            self.assertRaises(exceptions.ParameterMissing, mon.msg_received)
            args = {"service_name": "blorp", "message_id": "bla-blie-blub" }
            mon.msg_received(**args)
            f = open(mf)
            line = f.read()
            o = eval(line)
            self.assertDictEqual(o['args'], args)
            for k in ["time", "event", "status"]:
                self.assertIn(k, o)
            f.close()

if __name__ == '__main__':
    unittest.main()
