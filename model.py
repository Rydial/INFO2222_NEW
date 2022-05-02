
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

#-------------------------------------------------------------------------------

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
    if database.try_login(username, password) == True:
        # Set the User as Logged In
        database.set_online(username)

        return page_view("login_success", name=username)
    else:
        return page_view("login",
            fail_reason="Incorrect Username or Password. Please Try Again.")
        
#-------------------------------------------------------------------------------
# Register
#-------------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    return page_view("register", fail_reason="")

#-------------------------------------------------------------------------------

def register_check(username, password, confirmation):

    # Check if Password matches Password Confirmation
    if password != confirmation:
        return page_view("register",
            fail_reason="Passwords do not match. Please Try Again.")
    
    # Retrieve User's 'users' Table Entry
    user = database.search_table("users", "username", username)

    # Check if User exists
    if user is not None:
        return page_view("register",
            fail_reason="Username already exists. Please Try Again.")

    # Create a new User in the Database
    database.add_user(username, password)

    # Register Success
    return page_view("register_success", name=username)


def store_public_keys(username, encPubK, sigPubK):

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