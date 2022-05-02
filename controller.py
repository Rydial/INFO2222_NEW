

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


@post('/register')
def post_register():
    '''
        post_register
        
        Handles register attempts
        Expects a form containing 'username', 'password', and 'pwd_confirm'
        fields
    '''

    # Retrieve Necessary Fields
    username = request.forms.get("username")
    password = request.forms.get("password")
    confirmation = request.forms.get("pwd_confirm")

    # Call the appropriate method
    return model.register_check(username, password, confirmation)


@post('/public_keys.data')
def retrieve_public_keys():
    '''
    retrive_public_keys

    Fields are 'username', 'encPubK', and 'sigPubK'
    '''

    # Retrieve Form Field Values
    username = request.forms.get('username')
    encPubK = request.forms.get('encPubK')
    sigPubK = request.forms.get('sigPubK')

    # Call Appropriate Method
    return model.store_public_keys(username, encPubK, sigPubK)

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
