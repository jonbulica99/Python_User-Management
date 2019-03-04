from databases.mysql import Mysql

from objects.base import Base
from objects.user import User
from objects.state import State
from objects.group  import Group

def main():
    db = Mysql(database="user-manager2", user="root", pwd="", host="localhost")
    db.create_schema(Base)
    state = db.select_object(State).all()
    print(state)
    #db.remove_object(state[1])
    db.commit_changes()
   

if __name__ == "__main__":
    main()
