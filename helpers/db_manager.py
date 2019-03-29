from enum import Enum
from pydoc import locate
from utils.log import Logger
from utils.extras import safeformat


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

    def insert_default_values(self, db=None):
        from objects import State, User, Group, UserGroupLink, Host
        if not db:
            db = self.db
        db.log.debug("Adding default states to the database")
        states = [State(name=i) for i in __db_defaults__.get("states")]
        db.add_objects(states)
        state_present = db.select_object(State).filter_by(name="present").one()
        db.log.info("Added states: %s", ', '.join(i.name for i in states))

        db.log.debug("Adding default groups to the database")
        groups = [Group(name=i, state=state_present)
                  for i in __db_defaults__.get("groups")]
        db.add_objects(groups)
        group_dev = db.select_object(Group).filter_by(name="developers").one()
        db.log.info("Added groups: %s", ', '.join(i.name for i in groups))

        db.log.debug("Adding default users to the database")
        user_def_pass = self.config.parse_section(
            "users").get("default_password", None)
        users = [User(state=state_present, firstname=f, lastname=l,
                      password=user_def_pass) for f, l in __db_defaults__.get("users")]
        db.add_objects(users)
        user_rin = db.select_object(User).filter_by(username=users[2].username).one()
        db.log.info("Added users: %s", ', '.join(i.username for i in users))

        db.log.debug("Setting up user/group relationships")
        # by default every default user is also a member of the default group (developers)
        usergrouplinks = [UserGroupLink(user, group_dev)
                          for user in db.select_object(User).all()]
        db.add_objects(usergrouplinks)
        db.log.info("Added user/group relationships: %s",
                    ', '.join('uid: {u} => gid: {g}'.format(u=i.userid, g=i.groupid) for i in usergrouplinks))

        db.log.debug("Adding default hosts")
        hosts = [Host(name=name, address=ip, user=user_rin) for name, ip, in __db_defaults__.get("hosts")]
        db.add_objects(hosts)
        db.log.info("Added hosts: %s", ', '.join(i.name for i in hosts))

        db.session.refresh(user_rin)
        self.log.debug("User {} belogs to groups: {}".format(user_rin.username, ', '.join(i.name for i in user_rin.groups)))
        db.commit_changes()

    @staticmethod
    def db_supported_types():
        return [t for t in DbType]
