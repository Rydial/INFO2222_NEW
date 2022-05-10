
function getCookie(cookieName)
{
    let cookies = {};

    // Iterate through each Cookie
    document.cookie.split(';').forEach(function(cookie) {
      
        // Store Cookie as a Key:Value Pair
        let [key,value] = cookie.split('=');
        cookies[key.trim()] = value;
    })
    
    return cookies[cookieName];
}
