from databases.mysql import Mysql
from databases.sqlite import Sqlite
from databases.memory import Memory

from objects import *

from backends.ssh.main import SshBackend
from backends.ssh.commands import *

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

def testing():
    ssh_jbu = User(State('present'), 'Jon', 'Bulica', 'Shqiperia123', [])
    ssh_jbu.username = 'pi'
    localhost = Host('pi', '172.0.0.2', 22, ssh_jbu)
    ssh = SshBackend(host=localhost, user=ssh_jbu)
    ssh.connect()
    ssh.become(ssh.BecomeMethod.SUDO, ssh_jbu.password)

    add_user = UserAdd.from_user(ssh_jbu)
    add_user.username = 'ssh_jbu'
    ssh.run(add_user)
    exit(0)


if __name__ == "__main__":
    testing()
    # main()
    main_config = Config()
    manager = DatabaseManager(main_config.parse_section("database"))

    db = manager.create_database(DbType.MEMORY)
    db.connect()
    db.create_schema(Base)
