
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
    var username = document.getElementById('username').innerHTML;

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

/******************************************************************************/

// Generate the Key Pairs for the new User
generateKeyPairs().then(function() {
    // Key Pairs Generated
});