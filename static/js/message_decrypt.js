
function decodeString(encoded)
{
    return new TextDecoder().decode(encoded)
}


async function decryptMessage(data)
{
    // Retrieve Receiver's Username (Current Session Username)
    var receiver = getCookie('username');

    // Retrieve Receiver's Private Encryption Key
    var receiverEncPrivK = await crypto.subtle.importKey(
        'jwk',
        JSON.parse(localStorage.getItem(receiver + ':encPrivK')),
        {
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
        true,
        ['decrypt']
    );
    
    // Decrypt and Retrieve the Secret Key Plaintext
    var skRaw = await crypto.subtle.decrypt(
        {
            name: 'RSA-OAEP'
        },
        receiverEncPrivK,
        unpack(data['skCipher'])
    );

    // Import the Shared Secret Key
    var sharedSK = await crypto.subtle.importKey(
        'raw',
        skRaw,
        {
            name: 'AES-GCM'
        },
        true,
        ['encrypt', 'decrypt']
    );

    // Decrypt and Retrieve the Encoded Message
    var encodedMsg = await crypto.subtle.decrypt(
        {
            name: 'AES-GCM',
            iv: unpack(data['iv'])
        },
        sharedSK,
        unpack(data['msgCipher'])
    );

    // Retrieve Sender's Signing Public Key from the Server Database
    var senderSigPubK_JSON = await fetch('/user_public_key.json?' +
        'username=' + data['sender'] + '&' +'key_type=' + '2'
    ).then(response => response.json());

    // Import the Sender's Public Signing Key into JWK Format
    var senderSigPubK = await crypto.subtle.importKey(
        'jwk',
        senderSigPubK_JSON,
        {
            name: 'RSA-PSS',
            hash: 'SHA-256'
        },
        true,
        ['verify']
    );

    // Verify the Digital Signature with the Public Key
    var signatureVerified = await crypto.subtle.verify(
        {
            name: 'RSA-PSS',
            saltLength: 32,
        },
        senderSigPubK,
        unpack(data['signature']),
        encodedMsg
    );

    // Decode the Encoded Message into Plaintext
    var msg = decodeString(encodedMsg);

    // Check Digital Signature Verification
    if (signatureVerified == true)
        return [data['sender'], msg];
    else
        alert("Digital Signature could not be verified!");
}


async function retrieveMessages()
{
    // Retrieve Receiver Username (Current Session)
    var receiver = getCookie('username');

    // Retrieve Receiver's Messages
    var messageArray = await fetch(
        '/user_messages.json?username=' + receiver
    ).then(response => response.json());

    // Retrieve Active Card Name
    var active_card = document.getElementsByClassName('active_card')[0];
    var sender = active_card.getElementsByClassName('card_name')[0].innerHTML;

    // Retrieve Table
    var table = document.getElementById('inbox_table');
    
    // Clear Messages
    while (table.children.length > 1)
        table.removeChild(table.lastChild);

    // Iterate through each Encrypted Message (Format: JSON)
    for (var encryptedMsg of messageArray)
    {
        // Decrypt Encrypted Message
        var [user, msg] = await decryptMessage(encryptedMsg);

        if (user == sender)
        {
            // Create new Table Row
            var tr = document.createElement('tr');
            var td = document.createElement('td');
            td.innerText = msg;
            tr.append(td);

            // Add Table Row to Table
            table.append(tr);
        }
    }
}


function unpack(base64)
{
    return (new Uint8Array(atob(base64).split('').map(
        char => char.charCodeAt()))).buffer;
}
