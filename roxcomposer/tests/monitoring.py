# encoding: utf-8
#
# Monitoring test including tests for basic_monitoring and monitoring dependency injection.
#
# devs@droxit.de
#
# Copyright (c) 2018 droxIT GmbH
#


import unittest
import os
import roxcomposer.tests.classes.test_monitoring as test_monitoring
from os.path import join
from tempfile import TemporaryDirectory
from roxcomposer.monitor import basic_monitoring
from roxcomposer import exceptions


class TestMonitoring(unittest.TestCase):
 
    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_basic_monitoring(self):
        self.assertRaises(exceptions.ParameterMissing, basic_monitoring.BasicMonitoring)
        self.assertRaises(exceptions.ConfigError, basic_monitoring.BasicMonitoring, filename='/not/even/remotely/viable')
        self.assertRaises(exceptions.ParameterMissing, basic_monitoring.BasicReporting)
        self.assertRaises(exceptions.ConfigError, basic_monitoring.BasicReporting, filename='/not/even/remotely/viable')

        with TemporaryDirectory() as tdir:
            fname = 'monitoring_test.log'
            mf = join(tdir, fname)
            mon = basic_monitoring.BasicMonitoring(filename=mf)

            self.assertRaises(exceptions.ParameterMissing, mon.msg_received)
            args = {"service_name": "blorp", "message_id": "bla-blie-blub"}
            mon.msg_received(**args)
            f = open(mf)
            line = f.read()
            o = eval(line)
            self.assertDictEqual(o['args'], args)
            for k in ["time", "event", "status"]:
                self.assertIn(k, o)
            f.close()

            m_id = "prettycoolmessageid-adlkfjalsdfkj"
            args = {"service_name": "serv1", "message_id": m_id}
            mon.msg_received(**args)
            mon.msg_reached_final_destination(**args)
            custom = {"service_name": "serv1", "metric_name": "some_metric", "metric_dictionary":
                {"metric": "entry", "metric2": "another_entry"}}
            mon.custom_metric(**custom)

            self.assertRaises(exceptions.ParameterMissing, basic_monitoring.BasicReporting)
            rep = basic_monitoring.BasicReporting(filename=mf)
            self.assertEqual(rep.get_msg_history(message_id="invalidmsgid"), [])

            hist = rep.get_msg_history(message_id=m_id)
            self.assertEqual(len(hist), 2)
            for h in hist:
                self.assertEqual(h['args']['message_id'], m_id)
            self.assertEqual(rep.get_msg_status(message_id=m_id)['status'], "finalized")

            hist = rep.get_msg_history(message_id=None)
            self.assertEqual(len(hist), 1)
            for k in ["service_name", "metric_name", "metric_dictionary"]:
                self.assertIn(k, hist[0]['args'])
            for k in ["metric", "metric2"]:
                self.assertIn(k, hist[0]['args']["metric_dictionary"])

    @unittest.skipIf('SKIP_TEMPDIR_TEST' in os.environ, "tempdir issues")
    def test_monitoring_injection(self):
        with TemporaryDirectory() as tdir:
            monitor_path = join(tdir, 'monitor_test.log')
            log_path = join(tdir, 'monitor_test_log.log')

            params = {
                'name': 'monitortest',
                'ip': 'not important',
                'port': 7,
                'logging': {
                    'level': 'DEBUG',
                    'logpath': log_path
                },
                'monitoring': {
                    'filename': monitor_path,
                    'monitor_class': 'roxcomposer.tests.classes.dummy_monitor.DummyMonitor'
                }
            }

            mt = test_monitoring.MonitorTest(params)

            mt.do_receive()
            mt.do_dispatch()
            mt.do_destination()
            mt.do_error()

            f = open(monitor_path, "r")
            expected = ["DUMMY RECEIVE", "DUMMY DISPATCH", "DUMMY DESTINATION", "DUMMY ERROR"]
            for i, line in enumerate(f):
                self.assertEqual(line.strip(), expected[i])
            f.close()

            params = {
                'name': 'monitortest',
                'ip': 'not important',
                'port': 7,
                'monitoring': {
                    'filename': monitor_path,
                    'monitor_class': 'roxcomposer.tests.classes.dummy_monitor.NotExistentDummyMonitor'
                }
            }

            self.assertRaises(exceptions.ConfigError, test_monitoring.MonitorTest, params)

            params = {
                'name': 'monitortest',
                'ip': 'not important',
                'port': 7,
                'monitoring': {
                    'filename': monitor_path,
                    'monitor_class': None
                }
            }

            self.assertRaises(exceptions.ParameterMissing, test_monitoring.MonitorTest, params)

            params = {
                'name': 'monitortest',
                'ip': 'not important',
                'port': 7,
                'monitoring': {
                    'filename': monitor_path,
                    'monitor_class': 'roxcomposer.tests.classes.dummy_monitor.not_a_class'
                }
            }

            self.assertRaises(exceptions.NotAClass, test_monitoring.MonitorTest, params)


if __name__ == '__main__':
    unittest.main()
