from databases.mysql import Mysql
from databases.sqlite import Sqlite
from databases.memory import Memory

from objects.base import Base
from objects.user import User
from objects.state import State
from objects.group  import Group

from utils.config import Config
from helpers.db_manager import DatabaseManager, DbType

class UserManager(object):
    def __init__(self, config):
        self.config = config


def main():
    # db = Sqlite(file="user-manager")
    # db = Memory()
    db = Mysql(database="user-manager2", user="root", pwd="", host="localhost")
    db.connect()
    db.create_schema(Base)
    
    # add states
    states = [State(i) for i in ["present", "absent"]]
    db.add_objects(states)
    state_present = db.select_object(State).filter_by(name="present").one()
    print(state_present)

    user = User(state_present, "Max", "Mustermann", "hunter2", "")
    db.add_object(user)
    db.commit_changes()


if __name__ == "__main__":
    # main()
    main_config = Config()
    manager = DatabaseManager(main_config.parse_section("database"))

    db = manager.create_database(DbType.MEMORY)
    db.connect()
    db.create_schema(Base)
