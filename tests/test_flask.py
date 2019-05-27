import unittest

from helpers.db_manager import DatabaseManager, DbType
from main import app
from objects import State, User
from utils.config import Config


class FlaskTests(unittest.TestCase):
    main_config = Config()
    manager = DatabaseManager(main_config)
    database = None

    def setUp(self):
        # configure flask
        self.app = app.test_client()
        self.app.testing = True
        self.app.debug = False

        # setup database
        self.database = self.manager.create_database(db_type=DbType.MEMORY)
        self.database.connect(self.app.application)
        with self.app.application.app_context():
            self.database.create_schema()

        self.assertEqual(self.app.debug, False)

    def tearDown(self):
        pass

    def test_api_commands_insert_defaults(self):
        response = self.app.post(
            '/api/v1/cmd/insert_defaults', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data'], "insert_defaults")

    def test_api_users_empty(self):
        response = self.app.get('/api/v1/users/all', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data'], [])

    def test_api_users_default(self):
        self.test_api_commands_insert_defaults()
        response = self.app.get('/api/v1/users/all', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        # expect to find new user
        self.assertNotEqual(response.json['data'], [])

    def test_api_groups_empty(self):
        response = self.app.get('/api/v1/groups/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data'], [])

    def test_api_groups_default(self):
        self.test_api_commands_insert_defaults()
        response = self.app.get('/api/v1/groups/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        # expect to find new groups
        self.assertNotEqual(response.json['data'], [])

    def test_api_hosts_empty(self):
        response = self.app.get('/api/v1/hosts/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data'], [])

    def test_api_hosts_default(self):
        self.test_api_commands_insert_defaults()
        response = self.app.get('/api/v1/hosts/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertNotEqual(response.json['data'], [])
        # expect to find localhost
        self.assertEqual(response.json['data'][0]['name'], 'localhost')


if __name__ == "__main__":
    unittest.main()
