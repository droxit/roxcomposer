import unittest
from cli import commands
import mosaic.tests.classes.connector_dummy as connector_dummy


class TestCliCommands(unittest.TestCase):

    def setUp(self):
        self.server = connector_dummy.ConnectorDummy()
        self.server.start()

    def test_msg_history(self):
        print(commands.get_msg_history(*['msg_id']))

    def tearDown(self):
        self.server.stop()


if __name__ == '__main__':
    unittest.main()
