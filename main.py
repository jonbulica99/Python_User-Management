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
api = Api(app)


class UserEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('state', type=str)
    parser.add_argument('firstname', type=str)
    parser.add_argument('lastname', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('publicKey', type=str)

    def get(self, username):
        output = []
        if username == "all":
            for user in db.select_object(User).all():
                output.append(user.as_dict())
        else:
            output = db.select_object(User).filter_by(
                username=username).one().as_dict()
        return output

    def post(self, username):
        if username == "new":
            user = User(**self.parser.parse_args())
            return user


class GroupEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('parent', type=str)

    def get(self, id):
        output = []
        if not id:
            for group in db.select_object(Group).all():
                output.append(group.as_dict())
        else:
            output = db.select_object(Group).filter_by(id=id).one().as_dict()
        return output

    def post(self, id):
        if not id:
            group = Group(**self.parser.parse_args())
            return group
        else:
            return self.get(id)


class HostEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str)
    parser.add_argument('address', type=str)
    parser.add_argument('user', type=str)
    parser.add_argument('port', type=int)

    def get(self, id):
        output = []
        if not id:
            for host in db.select_object(Host).all():
                output.append(host.as_dict())
        else:
            output = db.select_object(Host).filter_by(id=id).one().as_dict()
        return output

    def post(self, id):
        if not id:
            host = Host(**self.parser.parse_args())
            return host
        else:
            return self.get(id)


class CommandEndpoint(Resource):
    def get(self, command):
        if command == "insert_defaults":
            manager.insert_default_values()
        elif command == "deploy_all":
            deploy()
        else:
            return {"Error": "Command %s not supported!" % command}


api.add_resource(UserEndpoint, '/api/v1/users/<string:username>')
api.add_resource(GroupEndpoint, '/api/v1/groups/<int:id>')
api.add_resource(HostEndpoint, '/api/v1/hosts/<int:id>')
api.add_resource(CommandEndpoint, '/api/v1/cmd/<string:command>')


def deploy():
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


if __name__ == "__main__":
    main_config = Config()

    # load db components
    manager = DatabaseManager(main_config)
    db = manager.create_database()
    db.connect()
    db.create_schema(Base)

    # start flask
    app.run(**main_config.parse_section("frontend"))

    exit(0)

    state_present = db.select_object(State).filter_by(name="present").one()

    # user to connect with
    # db.add_object(User(state_present, 'Jon', 'Bulica', 'Kennwort10!', username='jbu'))
    ssh_jbu = db.select_object(User).filter_by(username='jbu').one()

    # hosts = Host('Ubuntu-TEST01', '172.0.0.45', ssh_jbu), Host('Ubuntu-TEST02', '172.0.0.46', ssh_jbu)
    # db.add_objects(hosts)

    # db.commit_changes()
