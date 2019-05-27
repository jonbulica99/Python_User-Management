import unittest

from databases.sql_alchemy import SqlAlchemy
from databases.memory import Memory
from helpers.db_manager import DatabaseManager, DbType
from utils.config import Config
from objects import *
from flask import Flask


class DatabaseTests(unittest.TestCase):
    main_config = Config()
    manager = DatabaseManager(main_config)
    database = None
    app = Flask(__name__)

    def setUp(self):
        if not self.database:
            self.database = self.manager.create_database(db_type=DbType.MEMORY)
            self.database.connect(self.app)
        self.assertIsInstance(self.database, Memory)

    def test_initialize(self):
        self.assertIsInstance(self.database, SqlAlchemy)

    def test_schema(self):
        with self.app.app_context():
            try:
                self.database.create_schema()
            except Exception as e:
                self.fail("Failed to create the DB schema: " + e)

    def test_default_values(self):
        with self.app.app_context():
            # we need to run create schema first
            self.test_schema()
            try:
                self.manager.insert_default_values(self.database)
            except Exception as e:
                self.fail("Failed to insert default values: " + e)


if __name__ == '__main__':
    unittest.main()
