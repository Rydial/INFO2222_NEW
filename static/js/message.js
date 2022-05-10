
async function initFriendsList(username)
{
    // Retrieve All Other Usernames in the Server Database
    return fetch('/other_users.json?username=' + username)
    .then(response => response.json())
    .then(function(users)
    {
        // Retrieve Card List
        var cardList = document.getElementById('card_list');

        if (users.length > 0)
        {
            // Iterate through each User
            for (var user of users)
            {
                console.log(user['username']);
                console.log(user['muted']);

                // Create Card
                var card = document.createElement('ul');                

                if (user['muted'] == 'True')
                {
                    card.className = 'muted_card';

                    /* Create Card Avatar */
                    var card_avatar = document.createElement('img');
                    card_avatar.src = 'img/mute.png';
                }
                else
                {
                    card.className = 'friend_card';

                    /* Create Card Avatar */
                    var card_avatar = document.createElement('li');
                }

                card_avatar.className = 'card_avatar';

                /* Create Card Name */
                var card_name = document.createElement('li');
                card_name.className = 'card_name';
                card_name.innerHTML = user['username'];

                card.appendChild(card_avatar);
                card.appendChild(card_name);                

                // Append Card to Card List
                cardList.appendChild(card);
            }
        }
    });
}


function initCardClickEvents()
{
    // Retrieve Cards
    var cardList = document.getElementById('card_list');
    var cards = cardList.getElementsByClassName('friend_card');

    // Iterate through Cards
    for (var i = 0; i < cards.length; ++i)
    {
        // Attach function to 'click' Event
        cards[i].addEventListener('click', function()
        {
            // Retrieve Active Card
            var active_card = document.getElementsByClassName('active_card');
            
            if (active_card.length > 0)
            {
                /* Deselect Active Card */
                active_card[0].className = active_card[0].className.replace(
                    ' active_card', '');
            }
                
            // Select Current Card
            this.className += " active_card";

            /******************************************************************/

            // Change to Main Page
            changePage('main_page');
        });
    }
}

/******************************************************************************/

function initMessageUI()
{
    // Retrieve Current Session Username
    var username = getCookie('username');

    // Dynamically Populate the Friends List
    initFriendsList(username).then(function() {
        
        // Attach Click Events to each Friend Card
        initCardClickEvents();
    });
}

// Initialize Message UI
initMessageUI();

/******************************************************************************/

function changePage(page)
{
    // Retrieve Active Page
    var active_page = document.getElementsByClassName('active_page');

    if (active_page.length == 1)
    {
        // Deselect Active Page
        active_page[0].className = active_page[0].className.replace(
            ' active_page', '');
    }

    // Retrieve Specified Page
    var target_page = document.getElementById(page);

    // Set Main Page as Active Page
    target_page.className += " active_page";

    if (page == 'main_page')
    {
        // Set Page Name to Selected User's Name
        var main_page_name = target_page.getElementsByClassName(
            'page_name')[0];
        var active_card = document.getElementsByClassName('active_card')[0];
        var active_card_name = active_card.getElementsByClassName(
            'card_name')[0];
        main_page_name.innerHTML = active_card_name.innerHTML;
    }
    else if (page == 'inbox_page')
    {
        // Retrieve Messages send to the User
        retrieveMessages().then(function() {
            // Retrieved Messages
        });
    }
    else if (page == 'message_page')
        clearMessageOutput();
}


function clearMessageOutput()
{
    // Retrieve Message Output Element
    var msgOutput = document.getElementById('message_output');

    // Clear Output Text
    msgOutput.innerText = '';
}


function sendMessage()
{
    // Retrive Message Input
    var msgInput = document.getElementById('message_input');
    
    // Encrypt Message
    encryptMessage(msgInput.value).then(function()
    {
        // Display Message Sent Success
        var msgOutput = document.getElementById('message_output');
        msgOutput.innerText = 'Message Sent';

        // Clear Text Input
        msgInput.value = '';
    });
}
