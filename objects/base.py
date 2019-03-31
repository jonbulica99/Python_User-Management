from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class BaseObject:
    def __init__(self, *args, **kwargs):
        pass
    
    def as_dict(self, joins):
        pass

    def thread_safe_dict(self):
        return self.as_dict(joins=False)
