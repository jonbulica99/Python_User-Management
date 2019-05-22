from enum import Enum
from pydoc import locate
from utils.log import Logger
from utils.extras import safeformat
from objects import State, User, Group, UserGroupLink, Host


class DbType(Enum):
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MEMORY = "memory"
    POSTGRESQL = "postgresql"


__db_defaults__ = {
    "states": ["present", "absent", "inactive"],
    "users": [('Max', 'Mustermann'), ('Joseph', 'Schneemann'), ('Rin', 'Bros')],
    "groups": ["developers"],
    "hosts": [('localhost', '::1')]
}


class DatabaseManager:
    def __init__(self, config):
        self.log = Logger(self.__class__.__name__).get()
        self.config = config
        self.type = DbType(self.setting("type"))
        self.log.info("Loaded DatabaseManager with %s", self.type)
        self.db = None

    @staticmethod
    def db_supported_types():
        return [t for t in DbType]

    def setting(self, setting):
        db_conf = self.config.parse_section("database")
        if setting:
            return db_conf.get(setting)
        return db_conf

    def setup_database(self):
        import_string = "databases.{module}.{cls}"
        SqlAlchemyImpl = locate(import_string.format(
            module=self.type.value.lower(), cls=self.type.value.title()))
        self.db = SqlAlchemyImpl(**self.setting(None))
        return self.db

    def create_database(self, db_type=None, db_config={}):
        if db_type:
            self.type = DbType(db_type)
        if db_config or self.type == DbType.MEMORY:
            self.db_config = db_config
        return self.setup_database()

    def insert_default_values(self, database=None):
        if not database:
            database = self.db
        database.log.debug("Adding default states to the database")
        states = [State(name=i) for i in __db_defaults__.get("states")]
        database.add_objects(states)
        state_present = State.query.filter_by(name="present").one()
        database.log.info("Added states: %s",
                          ', '.join(i.name for i in states))

        database.log.debug("Adding default groups to the database")
        groups = [Group(name=i, state=state_present)
                  for i in __db_defaults__.get("groups")]
        database.add_objects(groups)
        group_dev = Group.query.filter_by(name="developers").one()
        database.log.info("Added groups: %s",
                          ', '.join(i.name for i in groups))

        database.log.debug("Adding default users to the database")
        user_def_pass = self.config.parse_section(
            "users").get("default_password", None)
        users = [User(state=state_present, firstname=f, lastname=l,
                      password=user_def_pass) for f, l in __db_defaults__.get("users")]
        database.add_objects(users)
        user_rin = User.query.filter_by(username=users[2].username).one()
        database.log.info("Added users: %s", ', '.join(
            i.username for i in users))

        database.log.debug("Setting up user/group relationships")
        # by default every default user is also a member of the default group (developers)
        usergrouplinks = [UserGroupLink(user, group_dev)
                          for user in User.query.all()]
        database.add_objects(usergrouplinks)
        database.log.info("Added user/group relationships: %s",
                          ', '.join('uid: {u} => gid: {g}'.format(u=i.userid, g=i.groupid) for i in usergrouplinks))

        database.log.debug("Adding default hosts")
        hosts = [Host(name=name, address=ip, user=user_rin)
                 for name, ip, in __db_defaults__.get("hosts")]
        database.add_objects(hosts)
        database.log.info("Added hosts: %s", ', '.join(i.name for i in hosts))

        self.log.debug("User %s belogs to groups: %s", user_rin.username, ', '.join(
            i.name for i in user_rin.groups))
        database.commit_changes()
