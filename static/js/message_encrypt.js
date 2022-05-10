
function encodeString(string)
{
    return new TextEncoder().encode(string)
}


async function encryptMessage(msg)
{
    // Retrieve Sender's Username (Session Username)
    var sender = getCookie('username');

    // Encode Plaintext Message
    var encodedMsg = encodeString(msg);

    // Retrieve the Sender's Signing Private Key
    var senderSigPrivK = await crypto.subtle.importKey(
        'jwk',
        JSON.parse(localStorage.getItem(sender + ':sigPrivK')),
        {
            name: 'RSA-PSS',
            hash: 'SHA-256'
        },
        true,
        ['sign']
    );

    // Sign the Encoded Message with the Sender's Signing Private Key
    var signature = await crypto.subtle.sign(
        {
            name: 'RSA-PSS',
            saltLength: 32,
        },
        senderSigPrivK,
        encodedMsg
    );

    // Generate an IV (Initialization Vector)
    var iv = crypto.getRandomValues(new Uint8Array(12));

    // Generate an AES Shared Secret Key
    var sharedSK = await crypto.subtle.generateKey(
        {
            name: 'AES-GCM',
            length: 256
        },
        true,
        ['encrypt', 'decrypt']
    );

    // Encrypt the Encoded Message with the Secret Key
    var msgCipher = await crypto.subtle.encrypt(
        {
            name: 'AES-GCM',
            iv: iv
        },
        sharedSK,
        encodedMsg
    );

    // Retrieve Receiver's Username
    var active_card = document.getElementsByClassName('active_card')[0];
    var receiver = active_card.getElementsByClassName('card_name')[0].innerHTML;

    // Retrieve Receiver's Encryption Public Key from the Server Database
    var receiverEncPubK_JSON = await fetch('/user_public_key.json?' +
        'username=' + receiver + '&' +'key_type=' + '1'
    ).then(response => response.json());

    // Import Receiver's Encryption Public Key into JWK Format
    var receiverEncPubK = await crypto.subtle.importKey(
        'jwk',
        receiverEncPubK_JSON,
        {
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
        true,
        ['encrypt']
    );

    // Export the Secret Key into Raw Format
    var skRaw = await crypto.subtle.exportKey(
        'raw',
        sharedSK
    );

    // Encrypt the Exported Secret Key with Receiver's Public Encryption Key
    var skCipher = await crypto.subtle.encrypt(
        {
            name: 'RSA-OAEP'
        },
        receiverEncPubK,
        skRaw
    );

    // Encapsulate Data into a JSON Object
    var encryptedMsg = {
        'sender': sender,
        'msgCipher': pack(msgCipher),
        'skCipher': pack(skCipher),
        'iv': pack(iv),
        'signature': pack(signature)
    };

    /* Prepare Data to be sent in a Form */
    var formData = new FormData();
    formData.append('receiver', receiver);
    formData.append('encryptedMsg', JSON.stringify(encryptedMsg));
    

    // Send Data to Server
    return fetch("/encrypted_message.data",
        {
            method: "POST",
            body: formData
        }
    );
}


function pack(arrayBuffer)
{
    return btoa(String.fromCharCode(...new Uint8Array(arrayBuffer)));
}
