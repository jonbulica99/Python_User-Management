from api.base import *


class GroupEndpoint(BaseEndpoint):
    __version__ = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument('id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('state', type=str)
        self.parser.add_argument('parent', type=dict)

    def get(self, id):
        if not id:
            output = []
            for group in Group.query.all():
                output.append(group.as_dict())
        else:
            output = Group.query.filter_by(id=id).one().as_dict()
        return self.return_success(output)

    def post(self, id):
        args = self.parser.parse_args()
        args.state = State.query.filter_by(name=args.state).one()
        if args.parent:
            args.parent = Group.query.filter_by(
                name=args.parent.get("name")).one()
        group = Group(**args)

        if self.Method(id) == self.Method.Add:
            errors = self.safe_add(group)
            if errors:
                return errors
            db_group = Group.query.filter_by(name=group.name).one()
            return self.safe_commit(db_group.as_dict())

        elif self.Method(id) == self.Method.Edit:
            db_group = Group.query.filter_by(id=args.get("id")).one()
            errors = self.safe_edit(group, db_group)
            if errors:
                return errors
            return self.safe_commit(group.as_dict())

        elif self.Method(id) == self.Method.Delete:
            db_group = Group.query.filter_by(id=args.get("id")).one()
            children = Group.query.filter_by(parent=db_group).all()
            if children:
                self.error_message = "Cannot delete group because it is parent of these other groups: {}.".format(
                    ', '.join(child.name for child in children))
                return self.return_error(Exception(self.error_message))

            errors = self.safe_delete(db_group)
            if errors:
                return errors
            return self.safe_commit(group.as_dict())
