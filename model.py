import json

import view
from no_sql_db import database

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-------------------------------------------------------------------------------
# Index
#-------------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-------------------------------------------------------------------------------
# Login
#-------------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login", fail_reason="")


def get_user_details(username) -> str:

    # Retrive User's 'users' Table Entry
    user = database.search_table("users", "username", username)

    # Encapsulate Values in JSON Format
    form = {
        'admin': str(bool(user[1])),
        'muted': str(bool(user[2])),
        'online': str(bool(user[-1]))
    }

    return json.dumps(form)


def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials,
        or a view for invalid credentials
    '''

    # Check User Login Credentials
    if (err := database.try_login(username, password)) != None:
        return page_view("login", fail_reason=err)
    else:
        # Set the User as Logged In
        database.set_online(username)

        return page_view("login_success", name=username)
        
#-------------------------------------------------------------------------------
# Register
#-------------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    return page_view("register")


def register_success_page(username):
    '''
        register_success_page
        Returns the view for the register_success_page
    '''
    return page_view("register_success", name=username)


def register_check(username, password):

    # Constants
    MAX_USERS = 8

    if len(database.tables['users'].entries) == MAX_USERS:
        return "Maximum User Capacity Reached. Cannot register any more users."
    
    # Retrieve User's 'users' Table Entry
    user = database.search_table("users", "username", username)

    # Check if User exists
    if user is not None:
        return "Username already exists. Please Try Again."

    # Create a new User in the Database
    database.add_user(username, password)

    print('-----------------------------')
    print(f"Created User: {username}")

    # Register Success
    return ""


def store_public_keys(username, encPubK, sigPubK):

    print(f"Storing Public Keys: {username}")

    # Let Server know public keys are being stored
    global publicKeysStored
    publicKeysStored = True

    # Add the Public Keys to the specified User
    return database.add_user_public_keys(username, encPubK, sigPubK)

#-------------------------------------------------------------------------------
# Message
#-------------------------------------------------------------------------------

def message_form():
    '''
        message_form
        Returns the view for the message_form
    '''
    return page_view("message")


def get_other_users(username):
    
    # Create a List of Usernames (Excluding Specified Username)
    users = []

    for entry in database.tables['users'].entries:
        # Extract Username
        other_username = entry[0]

        if other_username != username:

            # Encapsulate Values in a Form
            formData = {
                'username': entry[0],
                'admin': str(bool(entry[1])),
                'muted': str(bool(entry[2])),
                'online': str(bool(entry[-1]))
            }

            # Store Form in List
            users.append(formData)
    
    # Return a formatted string of Usernames
    return json.dumps(users)


def get_user_public_key(username, key_type) -> str:

    # Retrive Specified User Public Key
    entry = database.search_table('public_keys', 'username', username)

    return entry[key_type]


def get_user_messages(username):

    # Retrieve User Entry in 'messages' Table
    entry = database.search_table('messages', 'username', username)

    return entry[1]


def store_encrypted_message(receiver, encryptedMsg):

    # Retrieve Receiver Entry in the 'messages' Table
    entry = database.search_table('messages', 'username', receiver)

    # Append a new Message Entry into the Receiver's Messages
    if entry[1] == '[]':
        entry[1] = entry[1][:-1] + encryptedMsg + entry[1][-1:]
    else:
        entry[1] = entry[1][:-1] + ',' + encryptedMsg + entry[1][-1:]

    # Update Messages Database File
    database.update_messages_database()

    return

#-------------------------------------------------------------------------------
# Admin
#-------------------------------------------------------------------------------

def admin_form():
    '''
        admin_form
        Returns the view for the admin_form
    '''
    return page_view("admin")


def delete_user(username):
    
    print('-----------------------------')
    print(f"Deleting User: {username}")
    
    # Remove User Entry from every Table
    for table in database.tables:
        entry = database.search_table(table, 'username', username)
        database.tables[table].entries.remove(entry)

    # Remove All Messages Sent by the User
    for entry in database.tables['messages'].entries:
        
        # Retrieve Messages in JSON Format
        messages = json.loads(entry[1])
        
        # Filter out messages sent by the specified User
        entry[1] = json.dumps([x for x in messages if x['sender'] != username])

    # Update Every Database File
    database.update_users_database()
    database.update_passwords_database()
    database.update_public_keys_database()
    database.update_messages_database()


def mute_user(username):

    print('-----------------------------')
    print(f"Muting User: {username}")

    entry = database.search_table('users', 'username', username)

    entry[2] = 1

    # Update Every Database File
    database.update_users_database()


def unmute_user(username):

    print('-----------------------------')
    print(f"Unmuting User: {username}")

    entry = database.search_table('users', 'username', username)

    entry[2] = 0

    # Update Every Database File
    database.update_users_database()

#-------------------------------------------------------------------------------
# Logout
#-------------------------------------------------------------------------------

def logout_user(username):
    '''
        logout_user
        Returns the view for the logout_user
    '''

    # Set User Offline
    database.set_offline(username)

    return page_view("logout")

#-------------------------------------------------------------------------------
# Help
#-------------------------------------------------------------------------------

def help_form():
    '''
        help_form
        Returns the view for the help_form
    '''
    return page_view("help")

#-------------------------------------------------------------------------------
# About
#-------------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble="This is garble")

#-------------------------------------------------------------------------------
# Debug
#-------------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass

#-------------------------------------------------------------------------------
# 404
# Custom 404 error page
#-------------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
