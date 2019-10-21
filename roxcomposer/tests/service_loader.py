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
