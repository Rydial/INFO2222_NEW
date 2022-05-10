

from bottle import route, get, post, error, request, static_file
import model

#-------------------------------------------------------------------------------
# Static file paths
#-------------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-------------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-------------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-------------------------------------------------------------------------------
# Index
#-------------------------------------------------------------------------------

@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-------------------------------------------------------------------------------
# Login
#-------------------------------------------------------------------------------

@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()


@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.login_check(username, password)


@get('/user_details.json')
def get_user_details():
    '''
        get_user_details
        Param: 'username'
        Return Specified User's Details
    '''
    
    # Retrieve Username from Query Paramters
    username = request.query['username']

    return model.get_user_details(username)

#-------------------------------------------------------------------------------
# Register
#-------------------------------------------------------------------------------

@get('/register')
def get_register_controller():
    '''
        get_register
        
        Serves the register page
    '''
    return model.register_form()


@get('/register_success')
def get_register_success():
    '''
        get__register_success
        
        Params: 'username'
    '''

    # Retrieve Form Field Values
    username = request.query['username']

    # Call Appropriate Function
    return model.register_success_page(username) 


@post('/register')
def post_register():
    '''
        post_register
        
        Handles register attempts
        Expects a form containing 'username', 'password'
        fields
    '''

    # Retrieve Necessary Fields
    username = request.forms.get("username")
    password = request.forms.get("password")

    # Call the appropriate method
    return model.register_check(username, password)


@post('/public_keys.data')
def post_public_keys():
    '''
    post_public_keys

    Fields: 'username', 'encPubK', 'sigPubK'
    '''

    # Retrieve Form Field Values
    username = request.forms.get('username')
    encPubK = request.forms.get('encPubK')
    sigPubK = request.forms.get('sigPubK')

    # Call Appropriate Method
    model.store_public_keys(username, encPubK, sigPubK)

#-------------------------------------------------------------------------------
# Message
#-------------------------------------------------------------------------------

@get('/message')
def get_message_controller():
    '''
        get_message
        
        Serves the message page
    '''
    return model.message_form()


@get('/other_users.json')
def get_other_users():
    '''
        get_other_users
        Param: 'username'
        Return Every Username excluding Specified Username
    '''

    # Retrieve Username from Query Paramters
    username = request.query['username']

    return model.get_other_users(username)


@get('/user_public_key.json')
def get_user_public_key():
    '''
        get_user_public_key
        Param: 'username', 'key_type'
        Return Specified User Public Key
    '''
    
    # Retrieve Username from Query Paramters
    username = request.query['username']
    key_type = request.query['key_type']

    return model.get_user_public_key(username, int(key_type))


@get('/user_messages.json')
def get_user_messages():
    '''
        Param: 'username'
        
        Return Specified User's Messages
    '''
    
    # Retrieve Username from Query Paramters
    username = request.query['username']

    return model.get_user_messages(username)


@post('/encrypted_message.data')
def post_encrypted_message():
    '''
    Fields: 'receiver', 'encryptedMsg'
    '''

    # Retrieve Form Field Values
    receiver = request.forms.get('receiver')
    encryptedMsg = request.forms.get('encryptedMsg')

    # Call Appropriate Method
    model.store_encrypted_message(receiver, encryptedMsg)

#-------------------------------------------------------------------------------
# Admin
#-------------------------------------------------------------------------------

@get('/admin')
def get_admin_controller():
    '''
        get_admin
        
        Serves the admin page
    '''
    return model.admin_form()


@post('/delete_user.request')
def post_delete_user():
    '''
    Fields: 'username'
    '''

    # Retrieve Form Field Values
    username = request.forms.get('username')

    # Call Appropriate Method
    model.delete_user(username)


@post('/mute_user.request')
def post_mute_user():
    '''
    Fields: 'username'
    '''

    # Retrieve Form Field Values
    username = request.forms.get('username')

    # Call Appropriate Method
    model.mute_user(username)


@post('/unmute_user.request')
def post_unmute_user():
    '''
    Fields: 'username'
    '''

    # Retrieve Form Field Values
    username = request.forms.get('username')

    # Call Appropriate Method
    model.unmute_user(username)

#-------------------------------------------------------------------------------
# Logout
#-------------------------------------------------------------------------------

@get('/logout')
def get_logout_controller():
    '''
        get_logout
        
        Serves the logout page
    '''

    # Retrieve 'username' Cookie
    username = request.cookies['username']

    return model.logout_user(username)

#-------------------------------------------------------------------------------
# About
#-------------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()

#-------------------------------------------------------------------------------
# Debug
#-------------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-------------------------------------------------------------------------------
# 404
# Custom 404 error page
#-------------------------------------------------------------------------------

@error(404)
def error(error): 
    return model.handle_errors(error)
