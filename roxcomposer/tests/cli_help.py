# |------------------- OPEN SOURCE LICENSE DISCLAIMER -------------------|
# |                                                                      |
# | Copyright (C) 2019  droxIT GmbH - devs@droxit.de                     |
# |                                                                      |
# | This file is part of ROXcomposer.                                    |
# |                                                                      |
# | ROXcomposer is free software: you can redistribute it and/or modify  |
# | it under the terms of the GNU General Public License as published by |
# | the Free Software Foundation, either version 3 of the License, or    |
# | (at your option) any later version.                                  |
# |                                                                      |
# | This program is distributed in the hope that it will be useful,      |
# | but WITHOUT ANY WARRANTY; without even the implied warranty of       |
# | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the         |
# | GNU General Public License for more details.                         |
# |                                                                      |
# | You have received a copy of the GNU General Public License           |
# | along with this program. See also <http://www.gnu.org/licenses/>.    |
# |                                                                      |
# |----------------------------------------------------------------------|

import unittest
import cli.commands as cmd


class TestCliHelp(unittest.TestCase):
    def test_help(self):
        commands = list(cmd.cmd_map.keys())
        help_commands = [w.strip() for w in cmd.run_cmd('help').split("\n")][1:]

        self.assertEqual(sorted(commands), help_commands)

    def test_help_commands(self):
        commands = list(cmd.cmd_map.keys())
        for command in commands:
            doc_string = cmd.run_cmd('help', command)
            self.assertTrue(doc_string.startswith(command))

    def test_help_wrong_command(self):
        command = "NOT IN CMD MAP"
        doc_string = cmd.run_cmd('help', command)
        self.assertTrue(command in doc_string)
        self.assertTrue('not defined' in doc_string)

    def test_help_args(self):
        doc_string = cmd.run_cmd('help', 'cmd1', 'cmd2')
        self.assertTrue('superfluous arguments' in doc_string)

if __name__ == '__main__':
    unittest.main()
