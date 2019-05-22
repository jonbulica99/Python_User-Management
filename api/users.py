from api.base import *


class UserEndpoint(BaseEndpoint):
    __version__ = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument('id', type=str)
        self.parser.add_argument('state', type=str)
        self.parser.add_argument('firstname', type=str)
        self.parser.add_argument('lastname', type=str)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('publicKey', type=str)
        self.parser.add_argument('groups', type=dict, action="append")

    def get(self, username):
        if username == "all":
            output = []
            for user in User.query.all():
                output.append(user.as_dict())
        else:
            output = User.query.filter_by(username=username).one().as_dict()
        return self.return_success(output)

    def post(self, username):
        args = self.parser.parse_args()
        # get state from DB
        args.state = State.query.filter_by(name=args.state).one()
        user = User(**args)

        if username == "new":
            # insert to DB
            errors = self.safe_add(user)
            if errors:
                return errors

            db_user = User.query.filter_by(username=user.username).one()
            # add user, group relationship
            if args.groups:
                groups = args.groups
                for group in groups:
                    group = Group.query.filter_by(id=group.get('id')).one()
                    self.db.add_object(UserGroupLink(db_user, group))

            # no errors until now, so commit the changes
            return self.safe_commit(db_user.as_dict())

        elif username == "edit":
            db_user = User.query.filter_by(id=args.get("id")).one()
            errors = self.safe_edit(user, db_user)
            if errors:
                return errors

            # edit user, group relationship(s)
            if args.groups:
                # first delete existing relationships
                for rel in UserGroupLink.query.filter_by(userid=db_user.id).all():
                    self.safe_delete(rel)
                # add updated groups
                groups = args.groups
                for group in groups:
                    group = Group.query.filter_by(id=group.get('id')).one()
                    self.safe_add(UserGroupLink(db_user, group))

            # finally commit the changes
            return self.safe_commit(user.as_dict())

        elif username == "delete":
            db_user = User.query.filter_by(id=args.get("id")).one()
            hosts = Host.query.filter_by(user=db_user).all()
            if hosts:
                self.error_message = "Cannot delete user because these hosts are using it: {}.".format(
                    ', '.join(host.name for host in hosts))
                return self.return_error(Exception(self.error_message))
            errors = self.safe_delete(db_user)
            if errors:
                return errors
            return self.safe_commit(user.as_dict())
