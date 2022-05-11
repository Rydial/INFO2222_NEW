
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
var btn = document.getElementById(relativePath + 'NavBtn');

if (btn != null)
    btn.className += ' active_btn';


var dark_mode = localStorage.getItem('dark_mode');

if (dark_mode != null && dark_mode == 'True')
{
    document.body.className += ' dark_mode';
}


var enlarged_text = localStorage.getItem('enlarged_text');

if (enlarged_text != null && enlarged_text == 'True')
{
    document.body.className += ' enlarged_text';
}

/******************************************************************************/

function toggleDarkMode()
{
    var dark_mode = localStorage.getItem('dark_mode');

    if (dark_mode == null || dark_mode == 'False')
    {
        localStorage.setItem('dark_mode', 'True');

        document.body.className += ' dark_mode';
    }
    else
    {
        localStorage.setItem('dark_mode', 'False');

        document.body.className = document.body.className.replace(
            ' dark_mode', '');
    }
}


function toggleTextMode()
{
    var enlarged_text = localStorage.getItem('enlarged_text');

    if (enlarged_text == null || enlarged_text == 'False')
    {
        localStorage.setItem('enlarged_text', 'True');

        document.body.className += ' enlarged_text';
    }
    else
    {
        localStorage.setItem('enlarged_text', 'False');

        document.body.className = document.body.className.replace(
            ' enlarged_text', '');
    }
}
    