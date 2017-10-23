#!/usr/bin/env python3.5

import unittest
from mosaic import service_loader
from mosaic import errors


class TestBaseService(unittest.TestCase):
    def test_load_class(self):
#        self.assertRaises(errors.ParameterMissing, service_loader.load_class, None)
        self.assertRaises(ModuleNotFoundError, service_loader.load_class, 'totally.bogus.classpath')
        self.assertRaises(AttributeError, service_loader.load_class, 'logging.missingClassThingy')
 #       self.assertRaises(errors.NotAClass, service_loader.load_class, 'logging.info')

        param = {'blub': 2, 'blorp': "yeah"}
        c = service_loader.make_service_instance('mosaic.tests.classes.service_loader_test.DummyClass', param)
        self.assertEqual(param,c.get_args())


if __name__ == '__main__':
    unittest.main()
