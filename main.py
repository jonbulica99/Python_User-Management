#!/usr/bin/env python3
from backends.ssh.commands import *
from backends.ssh.main import SshBackend

from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse

from helpers.db_manager import DatabaseManager, DbType
from helpers.user_manager import UserManager
from objects import *
from utils.config import Config

app = Flask(__name__)
CORS(app)
api = Api(app)


class UserEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('firstname', type=str)
    parser.add_argument('lastname', type=str)
    parser.add_argument('password', type=str)
    parser.add_argument('publicKey', type=str)
    parser.add_argument('groups', type=dict, action="append")

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
        args = self.parser.parse_args()
        # get state from DB
        args.state = db.select_object(State).filter_by(name=args.state).one()
        user = User(**args)

        if username == "new":
            # insert to DB
            db.add_object(user)
            db_user = db.select_object(User).filter_by(
                username=user.username).one()
            # add user, group relationship
            if args.groups:
                groups = args.groups
                for group in groups:
                    group = db.select_object(
                        Group).filter_by(id=group.get('id')).one()
                    db.add_object(UserGroupLink(db_user, group))

            # no errors until now, so commit the changes
            db.commit_changes()
            return {"success": True, "user": user.as_dict()}

        elif username == "edit":
            db_user = db.select_object(User).filter_by(id=args.get("id")).one()
            for column in user.__table__.columns:
                if column.name != 'id':
                    setattr(db_user, column.name,
                            user.as_dict().get(column.name))

            # edit user, group relationship
            if args.groups:
                # first delete existing groups
                current_groups = db.select_object(
                    UserGroupLink).filter_by(userid=db_user.id).all()
                db.remove_objects(current_groups)
                # add updated groups
                groups = args.groups
                for group in groups:
                    group = db.select_object(Group).filter_by(
                        id=group.get('id')).one()
                    db.add_object(UserGroupLink(db_user, group))
            db.commit_changes()
            return {"success": True}

        elif username == "delete":
            db_user = db.select_object(User).filter_by(id=args.get("id")).one()
            db.remove_object(db_user)
            try:
                db.commit_changes()
            except Exception as e:
                return {
                    "success": False,
                    "message": "Could not delete user because a host is using it.",
                    "exception": str(e)
                }
            return {"success": True}


class GroupEndpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)
    parser.add_argument('name', type=str)
    parser.add_argument('state', type=str)
    parser.add_argument('parent', type=dict)

    def get(self, id):
        output = []
        if not id:
            for group in db.select_object(Group).all():
                output.append(group.as_dict())
        else:
            output = db.select_object(Group).filter_by(id=id).one().as_dict()
        return output

    def post(self, id):
        _translate = {
            0: "new",
            1: "edit",
            2: "delete"
        }
        args = self.parser.parse_args()
        print("DHERE", args)
        args.state = db.select_object(State).filter_by(name=args.state).one()
        if args.parent:
            args.parent = db.select_object(Group).filter_by(
                name=args.parent.get("name")).one()
        group = Group(**args)
        if _translate.get(id) == "new":
            try:
                db.add_object(group)
                db.commit_changes()
            except Exception as e:
                return {"success": False, "message": str(e)}

            db_group = db.select_object(Group).filter_by(name=group.name).one()
            return {"success": True, "group": db_group.as_dict()}

        elif _translate.get(id) == "edit":
            db_group = db.select_object(Group).filter_by(id=args.get("id")).one()
            for column in group.__table__.columns:
                if column.name != 'id':
                    setattr(db_group, column.name, group.as_dict().get(column.name))
            try:
                db.commit_changes()
            except Exception as e:
                return {"success": False, "message": str(e)}

            return {"success": True, "group": db_group.as_dict()}
        elif _translate.get(id) == "delete":
            db_group = db.select_object(Group).filter_by(id=args.get("id")).one()
            db.remove_object(db_group)
            try:
                db.commit_changes()
            except Exception as e:
                return {
                    "success": False,
                    "message": "Could not delete group because it's parent of other groups.",
                    "exception": str(e)
                }
            return {"success": True}



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
        _translate = {
            0: "new",
            1: "edit",
            2: "delete"
        }
        if _translate.get(id) == "new":
            host = Host(**self.parser.parse_args())
            return host
        else:
            return self.get(id)


class CommandEndpoint(Resource):
    def get(self, command):
        if command == "insert_defaults":
            db.create_schema(Base)
            manager.insert_default_values()
        elif command == "deploy_all":
            deploy()
        elif command == "save_all":
            db.commit_changes()
        else:
            return {"Error": "Command '%s' not supported!" % command}


api.add_resource(UserEndpoint, '/api/v1/users/<string:username>')
api.add_resource(GroupEndpoint, '/api/v1/groups/<int:id>')
api.add_resource(HostEndpoint, '/api/v1/hosts/<int:id>')
api.add_resource(CommandEndpoint, '/api/v1/cmd/<string:command>')


def deploy():
    hosts = db.select_object(Host).filter(
        ~Host.name.contains('localhost')).all()
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
