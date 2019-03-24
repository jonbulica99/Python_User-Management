import unittest

from databases.sql_alchemy import SqlAlchemy
from helpers.db_manager import DatabaseManager, DbType
from utils.config import Config
from objects import *


class DatabaseTests(unittest.TestCase):
    main_config = Config()
    manager = DatabaseManager(main_config)
    database = None

    def create_db(self):
        if not self.database:
            self.database = self.manager.create_database(db_type=DbType.MEMORY)
            self.database.connect()
        return self.database

    def test_initialize(self):
        db = self.create_db()
        self.assertIsInstance(db, SqlAlchemy)

    def test_schema(self):
        db = self.create_db()
        try:
            db.create_schema(Base)
        except Exception as e:
            self.fail("Failed to create the DB schema: " + e)

    def test_default_values(self):
        db = self.create_db()

        # TODO: warum brauchen wir dies?
        self.test_schema()
        try:
            self.manager.insert_default_values(db)
        except Exception as e:
            self.fail("Failed to insert default values: " + e)

 
if __name__ == '__main__':
    unittest.main()
