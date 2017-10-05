#!/usr/bin/env python3.5

import unittest
import re
from os.path import join
from tempfile import TemporaryDirectory
from mosaic.tests.classes.test_logging import LogTest
from mosaic import exceptions


class TestBaseService(unittest.TestCase):
 
    def test_logging(self):

        with TemporaryDirectory() as tdir:
            log_path = join(tdir, 'logtest.log')

            params = {
                'name': 'logtest',
                'ip': 'not important',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path
                }
            }

            lt = LogTest(params)
            f = open(log_path, "r")

            msg = 'simple message' 
            lt.logdebug(msg)
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('DEBUG', logline, "log level missing/or incorrect")

            lt.loginfo(msg)
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('INFO', logline, "log level missing/or incorrect")

            lt.logwarn(msg)
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('WARN', logline, "log level missing/or incorrect")

            lt.logerror(msg)
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('ERROR', logline, "log level missing/or incorrect")

            lt.logcritical(msg)
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('CRITICAL', logline, "log level missing/or incorrect")

            #### TODO: use this snippet after switching to ISO 8601 timestamps
            #iso_timestamp_re = re.compile("^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|(?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)$")
            #self.assertRegex(msg_in, iso_timestamp_re)

            f.close()

if __name__ == '__main__':
    unittest.main()
