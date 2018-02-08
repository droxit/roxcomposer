import unittest
import re
import time
import os
from os.path import join
from tempfile import TemporaryDirectory
from mosaic.tests.classes import test_logging


class TestLogging(unittest.TestCase):
 
    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_basic_logger(self):

        with TemporaryDirectory() as tdir:
            log_path = join(tdir, 'logtest.log')

            params = {
                'name': 'logging_logtest',
                'ip': 'not important',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path
                }
            }

            lt = test_logging.LogTest(params)
            f = open(log_path, "r")

            msg = 'simple message' 
            lt.logdebug(msg)
            logline = f.readline() # skip startup message
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

    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_logging_injection(self):
        with TemporaryDirectory() as tdir:
            log_path = join(tdir, 'logtest.log')

            params = {
                'name': 'logtest',
                'ip': 'not important',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path,
                    'logger_class': 'mosaic.tests.classes.dummy_logger.DummyLog'
                }
            }

            lt = test_logging.LogTest(params)

            msg = 'simple message'
            lt.logdebug(msg)
            f = open(log_path, "r")
            logline = f.readline()
            self.assertEqual(msg, logline, "wrong log output")
            f.close()


if __name__ == '__main__':
    unittest.main()
