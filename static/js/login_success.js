
async function retrieveUsername()
{
    // Retrieve Logged In User's Username
    return document.getElementById('username').innerHTML;
}

// Retrieve User's Details
retrieveUsername().then(function(username) {
    fetch('/user_details.json?username=' + username)
        .then(response => response.json())
        .then(function(userData)
        {
            console.log(userData['admin']);

            // Store Login Details as Cookies
            document.cookie = "username=" + username + "; path=/";
            document.cookie = "admin=" + userData['admin'] + "; path=/";

            /******************************************************************/

            document.getElementById('loginNavBtn').style.display = "none";
            document.getElementById('messageNavBtn').style.display = "block";
            document.getElementById('logoutNavBtn').style.display = "block";
            
            if (userData['admin'] == 'True')
                document.getElementById('adminNavBtn').style.display = "block";
            else
                document.getElementById('adminNavBtn').style.display = "none";
    });
})
