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
        set up connection to the db file and create table if it does not exist
        """
        self.con = sqlite3.connect('./database.db', check_same_thread=False)  # Create connection to database file
        self.con.row_factory = sqlite3.Row # Change row manager

        self.cur = self.con.cursor()  # Cursor for data selection

        # Check if table already exists
        self.cur.execute(''' select count(name) from sqlite_master where type='table' and name='users' ''')

        if self.cur.fetchone()[0] != 1:
            self.cur.execute('''create table users (name, pswd, id, dob, nationality)''')

    def register(self, name, pswd, id, dob, nationality):
        """
        method to register new user to table

        :param name: name of user
        :type name: string
        :param pswd: unencrypted password used to login
        :type pswd: string
        :param id: citizen identification number
        :type id: string
        :param dob: Date of birth
        :type dob: string
        :param nationality: country of user
        :type nationality: string
        :rtype:
        """
        self.cur.execute('''insert into users values (:name, :pswd, :id, :dob, :nationality)''',
                         {"name": name, "pswd": pswd, "id": id, "dob": dob, "nationality": nationality})

        self.con.commit() # Must commit changes before it is reflected in table

    def search(self, name):
        """
        method to search for details of user

        :param name: name of person to acquire data of
        :type name: string
        :return: list of data according to the table row
        :rtype: list
        """
        self.cur.execute('''select * from users where name=:name''', {"name": name})

        return self.cur.fetchone()

    def checkpass(self, name, pswd):
        """
        method to check if entered password allows users to login

        :param name: string
        :type name: name of user used to login
        :param pswd: password of user used to login
        :type pswd: string
        :return: boolean of whether password is correct
        :rtype: boolean
        """
        self.cur.execute('''select pswd from users where name=:name''', {"name": name})

        if self.cur.fetchone():
            for p in self.cur.fetchone():
                if p == pswd:
                    return True
                else:
                    return False
        else:
            return False

    def closedb(self):
        """
        method to call at end of program to close table
        """
        self.con.close()

### Test functions ###
db = Database()

# Registration of test acc, preferably should pass input of user from a web login page
db.register("admin", "test", "S12345678A", "01-01-1998", "Singaporean")

'''
# Search with name of user
r = db.search("admin")

# # Results
print("Searching for user admin")
print("Results:")
print(r['name'])

# Checking whether login should be success
# print("Correct password check: " + str(db.checkpass("admin", "test")))
# print("Incorrect password check: " + str(db.checkpass("admin", "kglakg")))

# Need to close at the end
#db.closedb()
'''