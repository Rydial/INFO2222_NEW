
async function generateKeyPairs()
{
    // Generate Encryption Key Pair
    var encKeyPair = await crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 4096,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256"
        },
        true,
        ["encrypt", "decrypt"]
    );

    // Generate Signature Key Pair
    var sigKeyPair = await crypto.subtle.generateKey(
        {
            name: "RSA-PSS",
            modulusLength: 4096,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256"
        },
        true,
        ["sign", "verify"]
    );

    /* Export Keys into JSON Web Keys */
    var encPrivK = await crypto.subtle.exportKey('jwk', encKeyPair.privateKey);
    var encPubK = await crypto.subtle.exportKey('jwk', encKeyPair.publicKey);
    var sigPrivK = await crypto.subtle.exportKey('jwk', sigKeyPair.privateKey);
    var sigPubK = await crypto.subtle.exportKey('jwk', sigKeyPair.publicKey);

    // Retrieve Username
    var username = document.getElementById('username').value;

    /* Store Private Keys in localStorage */
    localStorage.setItem(username + ":encPrivK", JSON.stringify(encPrivK));
    localStorage.setItem(username + ":sigPrivK", JSON.stringify(sigPrivK));

    // Prepare Form to send to Server
    let formData = new FormData();

    formData.append('username', username);
    formData.append('encPubK', JSON.stringify(encPubK));
    formData.append('sigPubK', JSON.stringify(sigPubK));

    // Send Form to Server
    return fetch("/public_keys.data",
        {
            body: formData,
            method: "POST"
        }
    );
}


function registerUser()
{
    // Retrieve Input Values
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var pwd_confirm = document.getElementById('pwd_confirm').value;

    if (username.length == 0 || password.length == 0 || pwd_confirm.length == 0)
    {
        // Set Register Fail Reason
        document.getElementById('register_fail_reason').innerText = 
            "Please fill in the form.";

        return;
    }
    else if (password != pwd_confirm)
    {
        // Set Register Fail Reason
        document.getElementById('register_fail_reason').innerText =
            "Passwords do not match. Please try again.";

        return;
    }

    /**************************************************************************/

    // Encapsulate Input Values in a Form
    var formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    

    // Post Register Request to Server
    fetch("/register",
        {
            method: "POST",
            body: formData
        }
    ).then(response => response.text())
    .then(function(errMsg)
    {
        if (errMsg == '')
        {
            // Generate the Key Pairs for the new User
            generateKeyPairs().then(function()
            {
                // Clear Register Fail Reason
                document.getElementById('register_fail_reason').innerText = '';

                // Redirect User to Register Success Page
                window.location.href = '/register_success?username=' + username;
            });
        }
        else
        {
            // Set Register Fail Reason to the Error Message
            document.getElementById('register_fail_reason').innerText = errMsg;
        }
    });
}

/******************************************************************************/

// Retrieve Register Form
var form = document.getElementById('register_form');

// Iterate through Input Elements
for (var input of form.getElementsByTagName('input'))
{
    // Add Key Press Event Listener
    input.addEventListener('keypress', function(event)
    {
        if (event.key === "Enter")
        {
            // Cancel the default action, if needed
            event.preventDefault();
            
            // Simulate Click Event for the Register Button
            document.getElementById('register_button').click();
        }
    });
}
