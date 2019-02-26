from objects.user import User
from databases.filedb import FileDB

def main():
    user = User()
    db = FileDB("database.fs")
    root = db.connect()

    #db.add_object(user)
    db.remove_object(user)
    db.commit()
    print(root.items())


if __name__ == "__main__":
    main()
