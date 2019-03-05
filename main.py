from databases.mysql import Mysql

from objects.base import Base
from objects.user import User
from objects.state import State
from objects.group  import Group

def main():
    db = Mysql(database="user-manager2", user="root", pwd="", host="localhost")
    db.create_schema(Base)
    
    # add states
    states = [State(i) for i in ["present", "absent"]]
    db.add_objects(states)

    state_present = db.select_object(State).filter_by(name="present").one()
    print(state_present)

    user = User(state_present, "Max", "Mustermann", "hunter2", "")
    db.add_object(user)
    db.commit_changes()
   

if __name__ == "__main__":
    main()
