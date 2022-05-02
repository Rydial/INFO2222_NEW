
// Retrieve Username
var username = document.getElementById('username').innerHTML;

// Store Username as the Cookie "username"
document.cookie = "username=" + username + "; path=/";
