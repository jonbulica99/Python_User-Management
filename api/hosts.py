from api.base import *


class HostEndpoint(BaseEndpoint):
    __version__ = 0.1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument('id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('user', type=dict)
        self.parser.add_argument('port', type=int)

    def get(self, id):
        if not id:
            output = []
            for host in Host.query.all():
                output.append(host.as_dict())
        else:
            output = Host.query.filter_by(id=id).one().as_dict()
        return self.return_success(output)

    def post(self, id):
        args = self.parser.parse_args()
        args.user = User.query.filter_by(id=args.user.get("id")).one()
        host = Host(**args)

        if self.Method(id) == self.Method.Add:
            errors = self.safe_add(host)
            if errors:
                return errors
            db_host = Host.query.filter_by(name=host.name).one()
            return self.safe_commit(db_host.as_dict())

        elif self.Method(id) == self.Method.Edit:
            db_host = Host.query.filter_by(id=args.get("id")).one()
            errors = self.safe_edit(host, db_host)
            if errors:
                return errors
            return self.safe_commit(host.as_dict())

        elif self.Method(id) == self.Method.Delete:
            db_host = Host.query.filter_by(id=args.get("id")).one()
            errors = self.safe_delete(db_host)
            if errors:
                return errors
            return self.safe_commit(host.as_dict())
