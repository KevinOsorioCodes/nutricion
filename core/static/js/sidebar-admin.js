let floatButton = document.getElementById('expand-side-bar');

floatButton.addEventListener('click', () => {

    let bodycontainer = document.getElementById('body_container');
    let sidebar = document.getElementById('sidebar');
    let textmenu1 = document.getElementById('menu-selecttext-options1');
    let textmenu2 = document.getElementById('menu-selecttext-options2');
    let textmenu3 = document.getElementById('menu-selecttext-options3');
    let textmenu4 = document.getElementById('menu-selecttext-options4');
    let textmenu5 = document.getElementById('menu-selecttext-options5');
    let textmenu6 = document.getElementById('menu-selecttext-options6');
    let textmenu10 = document.getElementById('menu-selecttext-options10');
    let textmenu7 = document.getElementById('user-info-sb');
    let LogoUA = document.getElementById('LogoUA-sb');
    let photo = document.getElementById('profile_info_sidebar');
    let button = document.getElementById('end-session-sb-b');
    let LogoRSU = document.getElementById('LogoRSU');

    if (sidebar.classList.contains('to-left')) {
        bodycontainer.classList.remove('fullcontainer')
        textmenu1.classList.remove('closed')
        textmenu2.classList.remove('closed')
        textmenu3.classList.remove('closed')
        textmenu4.classList.remove('closed')
        textmenu5.classList.remove('closed')
        textmenu6.classList.remove('closed')
        textmenu10.classList.remove('closed')
        LogoRSU.classList.remove('closedLogoRSU')
        floatButton.classList.remove('closedmenubutton')
        setTimeout(function(){
            button.classList.remove('closedbutton')
            textmenu7.classList.remove('closed')
            photo.classList.remove('closedphoto')
            LogoUA.src = "/static/registration/img/Logo-UA2.png";
            LogoUA.classList.remove('closedLogoUA')
        }, 100);
    } else {
        bodycontainer.classList.add('fullcontainer')
        textmenu1.classList.add('closed')
        textmenu2.classList.add('closed')
        textmenu3.classList.add('closed')
        textmenu4.classList.add('closed')
        textmenu5.classList.add('closed')
        textmenu6.classList.add('closed')
        textmenu7.classList.add('closed')
        textmenu10.classList.add('closed')
        photo.classList.add('closedphoto')
        button.classList.add('closedbutton')
        LogoRSU.classList.add('closedLogoRSU')
        floatButton.classList.add('closedmenubutton')
        setTimeout(function(){
            LogoUA.src = "/static/registration/img/Logo-UA.png";
            LogoUA.classList.add('closedLogoUA')
        }, 100);
    }
});