#!/usr/bin/env python3
from objects import *

from backends.ssh.main import SshBackend
from backends.ssh.commands import *

from utils.config import Config
from helpers.user_manager import UserManager
from helpers.db_manager import DatabaseManager, DbType

from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)


if __name__ == "__main__":
    main_config = Config()
    app.run(**main_config.parse_section("frontend"))

    exit(0)

    manager = DatabaseManager(main_config)

    db = manager.create_database()
    db.connect()
    db.create_schema(Base)

    # manager.insert_default_values()

    state_present = db.select_object(State).filter_by(name="present").one()

    # user to connect with 
    # db.add_object(User(state_present, 'Jon', 'Bulica', 'Kennwort10!', username='jbu'))
    ssh_jbu = db.select_object(User).filter_by(username='jbu').one()

    # hosts = Host('Ubuntu-TEST01', '172.0.0.45', ssh_jbu), Host('Ubuntu-TEST02', '172.0.0.46', ssh_jbu)
    # db.add_objects(hosts)

    hosts = db.select_object(Host).filter(~Host.name.contains('localhost')).all()
    users = db.select_object(User).all()
    groups = db.select_object(Group).all()
    for host in hosts:
        ssh = SshBackend(host)
        ssh.connect()
        user_manager = UserManager(backend=ssh)

        for group in groups:
            user_manager.handle_group(group)

        for user in users:
            user_manager.handle_user(user)

    # db.commit_changes()
