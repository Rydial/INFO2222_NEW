
// Retrieve Login Detail Cookies
var username = getCookie('username');
var admin = getCookie('admin');

if (username == undefined)
{
    document.getElementById('loginNavBtn').style.display = "block";
    document.getElementById('messageNavBtn').style.display = "none";
    document.getElementById('logoutNavBtn').style.display = "none";
}
else
{
    document.getElementById('loginNavBtn').style.display = "none";
    document.getElementById('messageNavBtn').style.display = "block";
    document.getElementById('logoutNavBtn').style.display = "block";
}

if (admin == 'True')
    document.getElementById('adminNavBtn').style.display = "block";
else
    document.getElementById('adminNavBtn').style.display = "none";

/******************************************************************************/

var relativePath = location.href.split('/', 4)[3];

document.getElementById(relativePath + 'NavBtn').className += ' active_btn';
    