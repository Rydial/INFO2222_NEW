
async function initUsersList(username)
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
                // Create Card
                var card = document.createElement('ul');      
                card.className = 'user_card';          

                if (user['muted'] == 'True')
                    card.className += ' muted_card';

                /* Create Card Avatar */
                var card_avatar = document.createElement('canvas');
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
    var cards = cardList.getElementsByClassName('user_card');

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

            // Change User Page
            changeUserPage();
        });
    }
}


function initCanvasImages()
{
    var muteImg = new Image();
    muteImg.onload = imageLoaded;

    muteImg.src = 'img/mute.png';

    function imageLoaded()
    {
        var muted_cards = document.getElementsByClassName('muted_card');

        // Iterate through Muted Cards
        for (var card of muted_cards)
        {
            // Retrieve Muted Card Avatar
            var avatar = card.getElementsByClassName('card_avatar')[0];

            // Draw Mute Icon on the Avatar
            avatar.getContext('2d').drawImage(muteImg, 0, 0, 300, 150);
        }
    }
}

/******************************************************************************/

function initAdminUI()
{
    // Retrieve Current Session Username
    var username = getCookie('username');

    // Dynamically Populate the Users List
    initUsersList(username).then(function() {
        
        // Attach Click Events to each Friend Card
        initCardClickEvents();

        // Initialize Images
        initCanvasImages();
    });
}

// Initialize Admin UI
initAdminUI();

/******************************************************************************/

function changeUserPage()
{
    // Retrieve Main Page
    var main_page = document.getElementById('main_page');

    // Retrieve Active Card
    var active_card = document.getElementsByClassName('active_card');

    if (active_card.length > 0)
    {
        // Retrieve Active Card Name
        var active_card_name = active_card[0].getElementsByClassName(
            'card_name')[0];
        
        // Set Main Page Name
        main_page.getElementsByClassName('page_name')[0].innerHTML =
            active_card_name.innerHTML;
        
        // Display Main Page
        main_page.style.display = 'block';

        // Retrieve User Details
        fetch('/user_details.json?username=' + active_card_name.innerHTML)
        .then(response => response.json())
        .then(function(user)
        {
            if (user['muted'] == 'True')
            {
                // Switch Button to Unmute Mode
                var button = document.getElementById('mute_user_button');
                button.onclick = unmuteUser;
                button.innerText = 'Unmute User';
            }
            else
            {
                // Switch Button to Mute Mode
                var button = document.getElementById('mute_user_button');
                button.onclick = muteUser;
                button.innerText = 'Mute User';
            }
        });
    }
    else
    {
        // Hide Main Page
        main_page.style.display = 'none';
    }
}


function deleteUser()
{
    // Retrieve Active Card
    var active_card = document.getElementsByClassName('active_card')[0];

    // Retrieve Active Card Name
    var active_card_name = active_card.getElementsByClassName(
        'card_name')[0].innerHTML;

    // Delete User From Server Database
    var formData = new FormData();
    formData.append('username', active_card_name);
    
    fetch("/delete_user.request",
    {
        method: "POST",
        body: formData
    });    

    // Retrive User List
    user_list = document.getElementById('card_list');

    // Get Current Active Card Index
    delete_card_index = [...user_list.children].indexOf(active_card);

    // Remove Current Active Card
    user_list.removeChild(active_card);

    if (user_list.children.length > 0)
    {
        // Calculate new Index
        active_card_index = delete_card_index == 0 ? 0 : delete_card_index - 1;

        // Set Card in calculated Index as Active
        user_list.children[active_card_index].className += " active_card";
    }

    changeUserPage();
}


function muteUser()
{
    // Retrieve Active Card
    var active_card = document.getElementsByClassName('active_card')[0];
    active_card.className += ' muted_card';

    // Add Mute Icon
    var card_avatar =  active_card.getElementsByClassName('card_avatar')[0];
    var muteImg = new Image();
    muteImg.onload = imageLoaded;

    muteImg.src = 'img/mute.png';

    function imageLoaded()
    {
        card_avatar.getContext('2d').drawImage(muteImg, 0, 0, 300, 150);
    }

    // Retrieve Active Card Name
    var active_card_name = active_card.getElementsByClassName(
        'card_name')[0].innerHTML;

    var formData = new FormData();
    formData.append('username', active_card_name);
    
    fetch("/mute_user.request",
    {
        method: "POST",
        body: formData
    })
    .then(function()
    {
        changeUserPage();
    });
}


function unmuteUser()
{
    // Retrieve Active Card
    var active_card = document.getElementsByClassName('active_card')[0];
    active_card.className = active_card.className.replace(' muted_card', '');

    // Remove Mute Icon
    var card_avatar =  active_card.getElementsByClassName('card_avatar')[0];
    var unmuteImg = new Image();
    unmuteImg.onload = imageLoaded;

    unmuteImg.src = 'img/unmute.png';

    function imageLoaded()
    {
        card_avatar.getContext('2d').drawImage(unmuteImg, 0, 0, 300, 150);
    }

    // Retrieve Active Card Name
    var active_card_name = active_card.getElementsByClassName(
        'card_name')[0].innerHTML;

    var formData = new FormData();
    formData.append('username', active_card_name);
    
    fetch("/unmute_user.request",
    {
        method: "POST",
        body: formData
    })
    .then(function()
    {
        changeUserPage();
    });
}