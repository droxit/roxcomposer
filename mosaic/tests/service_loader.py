import unittest
from roxcomposer import service_loader
from roxcomposer import exceptions


class TestBaseService(unittest.TestCase):
    def test_load_class(self):
        self.assertRaises(exceptions.ParameterMissing, service_loader.load_class, None)
        self.assertRaises(exceptions.ConfigError, service_loader.load_class, 'totally.bogus.classpath')
        self.assertRaises(exceptions.NotAClass, service_loader.load_class, 'logging.info')

        param = {'blub': 2, 'blorp': "yeah"}
        c = service_loader.make_service_instance('roxcomposer.tests.classes.service_loader_test.DummyClass', param)
        self.assertEqual(param, c.get_args())


if __name__ == '__main__':
    unittest.main()
