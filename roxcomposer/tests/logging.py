# encoding: utf-8
#
# Logging test including tests for basic_logging and logging dependency injection.
#
# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU Lesser General Public License as       |
# | published by the Free Software Foundation, either version 3 of the   |
# | License, or (at your option) any later version.                      |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU Lesser General Public License    |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|
#

import unittest
import os
from os.path import join
from tempfile import TemporaryDirectory
from roxcomposer.tests.classes import test_logging
import roxcomposer.exceptions as exceptions


class TestLogging(unittest.TestCase):
 
    def test_basic_logger_fails(self):
        params = {
            'name': 'logger_should_fail',
            'ip': '127.0.0.1',
            'port': 3,
            'logging': {
                'level': 'WARNING',
                'logpath': '/does/not/exists.log'
            },
            'monitoring': {
                'filename': '/dev/null'
            }
        }

        self.assertRaises(exceptions.ConfigError, test_logging.LogTest, params)

        del params['logging']['logpath']
        params['logging']['level'] = 'totally dumb not existstant level name'

        self.assertRaises(exceptions.ConfigError, test_logging.LogTest, params)

    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_basic_logger(self):

        with TemporaryDirectory() as tdir:
            log_path = join(tdir, 'logtest.log')

            params = {
                'name': 'logging_logtest',
                'ip': '127.0.0.1',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'logpath': log_path
                },
                'monitoring': {
                    'filename': '/dev/null'
                }
            }

            lt = test_logging.LogTest(params)
            f = open(log_path, "r")

            msg = 'simple message' 
            lt.logdebug(msg)
            f.readline()  # skip startup message
            logline = f.readline()
            self.assertIn(msg, logline, "original message not contained in log line")
            self.assertIn('DEBUG', logline, "log level missing/or incorrect")

            lt.logdebug(msg, message_id='test-id')
            logline = f.readline()
            self.assertIn('test-id', logline, "message id not present in log line")

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

            # TODO: use this snippet after switching to ISO 8601 timestamps
            # iso_timestamp_re = re.compile("^(?:[1-9]\d{3}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1\d|2[0-8])|
            # (?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[1-9]\d(?:0[48]|[2468][048]|[13579][26])|
            # (?:[2468][048]|[13579][26])00)-02-29)T(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:Z|[+-][01]\d:[0-5]\d)$")
            # self.assertRegex(msg_in, iso_timestamp_re)

            f.close()

    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_logging_injection(self):
        with TemporaryDirectory() as tdir:
            log_path = join(tdir, 'logtest.log')

            params = {
                'name': 'logtest',
                'ip': '127.0.0.1',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'logpath': log_path,
                    'logger_class': 'roxcomposer.tests.classes.dummy_logger.DummyLog'
                },
                'monitoring': {
                    'filename': '/dev/null'
                }
            }

            lt = test_logging.LogTest(params)

            msg = 'simple message'
            lt.logdebug(msg)
            f = open(log_path, "r")
            logline = f.readline()
            self.assertEqual(msg, logline, "wrong log output")
            f.close()

            params = {
                'name': 'logtest',
                'ip': '127.0.0.1',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path,
                    'logger_class': 'roxcomposer.tests.classes.dummy_logger.NotExistentDummyLog'
                },
                'monitoring': {
                    'filename': '/dev/null'
                }
            }

            self.assertRaises(exceptions.ConfigError, test_logging.LogTest, params)

            params = {
                'name': 'logtest',
                'ip': '127.0.0.1',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path,
                    'logger_class': None
                },
                'monitoring': {
                    'filename': '/dev/null'
                }
            }

            self.assertRaises(exceptions.ParameterMissing, test_logging.LogTest, params)

            params = {
                'name': 'logtest',
                'ip': '127.0.0.1',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'filename': log_path,
                    'logger_class': 'roxcomposer.tests.classes.dummy_logger.not_a_class'
                },
                'monitoring': {
                    'filename': '/dev/null'
                }
            }

            self.assertRaises(exceptions.NotAClass, test_logging.LogTest, params)


if __name__ == '__main__':
    unittest.main()
