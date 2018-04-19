import unittest
import cli.commands as cmd


class TestCliHelp(unittest.TestCase):
    def test_help(self):
        commands = list(cmd.cmd_map.keys())
        help_commands = [w.strip() for w in cmd.run_cmd('help').split("\n")][1:]

        self.assertEqual(commands, help_commands)

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
