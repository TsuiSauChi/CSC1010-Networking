import sqlite3


class Database:
    """
    class for managing of data of users

    Columns for the database table includes:
    name of user, the password (NOT ENCRYPTED), ic number, date of birth, nationality


    con: connection object to database file

    cur: cursor object for data selection within file

    """

    def __init__(self):
        """

        """
        self.con = sqlite3.connect('../../Desktop/AY20 21/Tri 2/CSC1010 Computer Networks/Project/users.db')  # Create connection to database file
        self.con.row_factory = sqlite3.Row

        self.cur = self.con.cursor()  # Cursor for data selection

        self.cur.execute(''' select count(name) from sqlite_master where type='table' and name='users' ''')

        # if the count is 1, then table exists
        if self.cur.fetchone()[0] != 1:
            self.cur.execute('''create table users (name, pswd, id, dob, nationality)''')

    def register(self, name, pswd, id, dob, nationality):

        self.cur.execute('''insert into users values (:name, :pswd, :id, :dob, :nationality)''',
                         {"name": name, "pswd": pswd, "id": id, "dob": dob, "nationality": nationality})

        self.con.commit()

    def search(self, name):

        self.cur.execute('''select * from users where name=:name''', {"name": name})

        return self.cur.fetchone()

    def checkpass(self, name, pswd):

        self.cur.execute('''select pswd from users where name=:name''', {"name": name})

        for p in self.cur.fetchone():
            if p == pswd:
                return True
            else:
                return False

    def closedb(self):

        self.con.close()


db = Database()
db.register("admin", "test", "S12345678A", "01-01-1998", "Singaporean")
r = db.search("admin")

print("Searching for user admin")
print("Results:")
for x in r:
    print(x)

print("Correct password check: " + str(db.checkpass("admin", "test")))
print("Incorrect password check: " + str(db.checkpass("admin", "kglakg")))
db.closedb()
