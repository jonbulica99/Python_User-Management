import random
from api.base import *
from threading import Thread
from backends.ssh.main import SshBackend
from helpers.user_manager import UserManager


class DeployBackground(Thread):
    def __init__(self, context):
        super().__init__()
        self.log = Logger("DeployBackground").get()
        self.app = context
        self.progress = {
            "command": "deploy_all",
            "percent": 0.0,
            "current": {
                "host": None,
                "object": None
            },
            "success": [],
            "error": []
        }

    def run(self):
        with self.app.app_context():
            self.log.debug("Fetching all hosts...")
            hosts = Host.query.filter(~Host.name.contains('localhost')).all()
            self.log.debug("Fetching all users...")
            users = User.query.all()
            self.log.debug("Fetching all groups...")
            groups = Group.query.all()
            self.log.warning("Deployment started!")
            len_hosts = len(hosts)
            len_groups = len(groups)
            len_users = len(users)
            for i, host in enumerate(hosts, 1):
                self.progress["current"]["host"] = host.thread_safe_dict()
                try:
                    ssh = SshBackend(host=host)
                    ssh.connect()
                    user_manager = UserManager(backend=ssh)
                    for g, group in enumerate(groups, 1):
                        self.progress["percent"] = 0.5 * \
                            (g/len_groups)*i/len_hosts * 100
                        self.progress["current"]["object"] = group.thread_safe_dict(
                        )
                        user_manager.handle_group(group)
                    for u, user in enumerate(users, 1):
                        self.progress["percent"] = (
                            u/len_users)*i/len_hosts * 100
                        self.progress["current"]["object"] = user.thread_safe_dict()
                        user_manager.handle_user(user)
                    self.log.info("Deployment succeded for %s", host)
                    self.progress["success"].append(host.thread_safe_dict())
                except Exception as e:
                    self.log.error(
                        "Deployment failed for %s. Error %s", host, e)
                    self.progress["error"].append(host.thread_safe_dict())
                self.progress["percent"] = i/len_hosts * 100
                self.progress["current"] = {"host": None, "object": None}


class CommandEndpoint(BaseEndpoint):
    __version__ = 0.1

    class Command(Enum):
        InsertDefaults = "insert_defaults"
        DeployAll = "deploy_all"
        ForceCommit = "force_commit"
        ForceRollback = "force_rollback"

    threads = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parser.add_argument('thread', type=int)
        self.db = self.db_manager.db

    @classmethod
    def create(cls, database, app):
        cls.db_manager = database
        cls.app = app
        return cls

    def get(self, command):
        if self.Command(command) == self.Command.DeployAll:
            thread_id = self.parser.parse_args().get("thread")
            if thread_id:
                progress = self.threads[thread_id].progress
                progress["thread_id"] = thread_id
                if progress["error"] and not progress["current"]["host"]:
                    self.error_message = "Deployment failed for some hosts."
                    return self.return_error(Exception(self.error_message), data=progress)
                return self.return_success(progress)
            return self.return_error(Exception("Please provide a thread_id using the 'thread' parameter."))
        elif self.Command(command):
            return self.return_success({"percent": 100.0, "command": command})
        else:
            self.error_message = "Command '{}' not supported!".format(command)
            return self.return_error(Exception(self.error_message))

    def post(self, command):
        if self.Command(command) == self.Command.InsertDefaults:
            try:
                db.create_all()
                self.db_manager.insert_default_values()
            except Exception as e:
                self.error_message = "Something went wrong. Did you run this more than once?"
                return self.return_error(e)
        elif self.Command(command) == self.Command.DeployAll:
            return self.deploy_all(random.randint(0, 10000))
        elif self.Command(command) == self.Command.ForceCommit:
            return self.safe_commit({"forced": True})
        elif self.Command(command) == self.Command.ForceRollback:
            self.db.rollback_changes()
            return self.return_success(None)
        else:
            self.error_message = "Command '{}' not supported!".format(command)
            return self.return_error(Exception(self.error_message))
        # if no errors occured up to this point, assume everything went well
        return self.return_success(command)

    def deploy_all(self, thread_id):
        try:
            self.log.warning("Creating thread #%s", thread_id)
            self.threads[thread_id] = DeployBackground(self.app)
            self.threads[thread_id].start()
        except Exception as e:
            return self.return_error(e)
        return self.return_success(data=thread_id)
