import os
import hashlib

#-------------------------------------------------------------------------------

class Table():

    '''                          Init-Stage Methods                          '''

    def __init__(self, table_name, *table_fields):
        self.entries = []
        self.fields = table_fields
        self.name = table_name

    '''                            Class Methods                             '''

    def create_entry(self, data):
        '''
        Inserts an entry in the table
        Doesn't do any type checking
        '''

        # Bare minimum, we'll check the number of fields
        if len(data) != len(self.fields):
            raise ValueError('Wrong number of fields for table')

        self.entries.append(data)
        return


    def search_table(self, target_field_name, target_value):
        '''
            Search the table given a field name and a target value
            Returns the first entry found that matches
        '''
        # Lazy search for matching entries
        for entry in self.entries:
            for field_name, value in zip(self.fields, entry):
                if target_field_name == field_name and target_value == value:
                    return entry

        # Nothing Found
        return None

#-------------------------------------------------------------------------------

class DB():

    '''                          Init-Stage Methods                          '''

    def __init__(self):
        # Initialize Member Variables
        self.tables = {}

        # Read Data from Database CSV Files
        self.read_databases()
        
        return
    

    def read_databases(self):

        # Open the 'users' Database
        with open("data/users.csv", "a+") as file:

            # Set File Pointer to the Beginning of the File
            file.seek(0)

            # Create a new Table Entry "users" in the Database
            self.add_table("users",
                "username",
                "admin",
                "loggedIn"
            )

            # Add each 'entry' into the "users" Table
            for entry in file.readlines():

                # Split Entry into Variables
                user, admin, loggedIn = entry.strip().split(",")

                self.create_table_entry("users",
                    [user, int(admin), int(loggedIn)])
        
        #-----------------------------------------------------------------------

        # Open the 'passwords' Database
        with open("data/passwords.csv", "a+") as file:

            # Set File Pointer to the Beginning of the File
            file.seek(0)

            # Create a new Table Entry "passwords" in the Database
            self.add_table("passwords",
                "username",
                "password",
                "salt"
            )

            # Add each 'entry' into the "passwords" Table
            for entry in file.readlines():

                # Split Entry into Variables
                user, hash, salt = entry.strip().split(",")

                self.create_table_entry("passwords",
                    [user, bytes.fromhex(hash), bytes.fromhex(salt)])
        
        #-----------------------------------------------------------------------

        # Open the 'public_keys' Database
        with open("data/public_keys.csv", "a+") as file:

            # Set File Pointer to the Beginning of the File
            file.seek(0)

            # Create a new Table Entry "public_keys" in the Database
            self.add_table("public_keys",
                "username",
                "encPubK",
                "sigPubK"
            )

            # Add each 'entry' into the "public_keys" Table
            for entry in file.readlines():

                # Extract Fields
                username, keys = entry.strip().split(",", maxsplit=1)
                encPubK = keys[:keys.find('}') + 1]
                sigPubK = keys[keys.find('}') + 2:]

                self.create_table_entry("public_keys",
                    [username, encPubK, sigPubK])

            
        return

    '''                            Class Methods                             '''

    def add_table(self, table_name, *table_fields):
        '''
            Adds a table to the database
        '''
        table = Table(table_name, *table_fields)
        self.tables[table_name] = table

        return


    def add_user(self, username, password, admin=0):

        # Add a new Entry in the 'users' Database
        with open("data/users.csv", "a+") as file:
            file.write(",".join([username, str(admin), str(0)]))
        
        # Add new Entry to the "users" Table
        database.create_table_entry("users", [username, admin, 0])

        #-----------------------------------------------------------------------

        # Generate a random salt with a length of 32 bytes
        salt = os.urandom(32)

        # Hash the Password with the generated Salt
        hash = hashlib.pbkdf2_hmac(
            "sha256",                   # Hash Digest Algorithm
            password.encode("utf-8"),   # Password converted to Bytes
            salt,                       # Salt
            100000,                     # 100,000 iterations of SHA-256
            dklen=128                   # Get a 128 byte hash/key 
        )

        # Add a new Entry in the 'passwords' Database
        with open("data/passwords.csv", "a+") as file:
            file.write(",".join([username, hash.hex(), salt.hex()]))

        # Add new Entry to the "passwords" Table
        database.create_table_entry("passwords", [username, hash, salt])

        return


    def add_user_public_keys(self, username, encPubK, sigPubK):

        # Add a new Entry in the 'public_keys' Database
        with open("data/public_keys.csv", "a+") as file:
            file.write(",".join([username, encPubK, sigPubK]))

        # Add new Entry to the "public_keys" Table
        database.create_table_entry("public_keys", [username, encPubK, sigPubK])

        return


    def create_table_entry(self, table_name, data):
        '''
            Calls the create entry method on the appropriate table
        '''
        return self.tables[table_name].create_entry(data)


    def search_table(self, table_name, target_field_name, target_value):
        '''
            Calls the search table method on an appropriate table
        '''
        return self.tables[table_name].search_table(
            target_field_name, target_value)


    def set_offline(self, username):

        # Retrieve User's Table Entry
        user = self.search_table("users", "username", username)

        # Set the User's Status as Offline
        user[-1] = 0

        # Update Database File
        self.update_database()

        return


    def set_online(self, username):

        # Retrieve User's Table Entry
        user = self.search_table("users", "username", username)

        # Set the User's Status as Online
        user[-1] = 1

        # Update Database File
        self.update_database()

        return


    def try_login(self, username, password):

        # Retrieve User's 'users' Table Entry
        user = self.search_table("users", "username", username)

        # Check Username
        if user is None:
            return False

        # Check if User is already Logged in
        if user[-1]:
            return False

        # Retrieve User's 'passwords' Table Entry
        user = self.search_table("passwords", "username", username)

        # Hash the Input Password with the stored Salt
        input_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            user[2],
            100000,
            dklen=128)
        
        # Check Password
        if input_hash != user[1]:
            return False

        return True


    def update_database(self):

        with open("data/users.csv", "w") as file:
            for user, admin, loggedIn in self.tables['users'].entries:
                file.write(",".join([user, str(admin), str(loggedIn)]))
        
        with open("data/passwords.csv", "w") as file:
            for user, hash, salt in self.tables['passwords'].entries:
                file.write(",".join([user, hash.hex(), salt.hex()]))

        with open("data/public_keys.csv", "w") as file:
            for user, encPubK, sigPubK in self.tables['public_keys'].entries:
                file.write(",".join([user, encPubK, sigPubK]))

        return

#-------------------------------------------------------------------------------

# Our global database
database = DB()
