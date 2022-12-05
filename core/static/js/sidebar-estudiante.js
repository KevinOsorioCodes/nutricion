let floatButton = document.getElementById('expand-side-bar');

floatButton.addEventListener('click', () => {

    let bodycontainer = document.getElementById('body_container');
    let sidebar = document.getElementById('sidebar');
    let textmenu1 = document.getElementById('menu-selecttext-options1');
    let textmenu7 = document.getElementById('user-info-sb');
    let textmenu9 = document.getElementById('menu-selecttext-options9');
    let textmenu10 = document.getElementById('menu-selecttext-options10');
    let textmenuc = document.getElementById('menu-selecttext-optionsc');
    let LogoUA = document.getElementById('LogoUA-sb');
    let photo = document.getElementById('profile_info_sidebar');
    let button = document.getElementById('end-session-sb-b');
    let LogoRSU = document.getElementById('LogoRSU');

    if (sidebar.classList.contains('to-left')) {
        bodycontainer.classList.remove('fullcontainer')
        textmenu1.classList.remove('closed')
        textmenu9.classList.remove('closed')
        textmenu10.classList.remove('closed')
        textmenuc.classList.remove('closed')
        LogoRSU.classList.remove('closedLogoRSU')
        floatButton.classList.remove('closedmenubutton')
        setTimeout(function(){
            textmenu7.classList.remove('closed')
            button.classList.remove('closedbutton')
            photo.classList.remove('closedphoto')
            LogoUA.src = "/static/registration/img/Logo-UA2.png";
            LogoUA.classList.remove('closedLogoUA')
        }, 100);
    } else {
        bodycontainer.classList.add('fullcontainer')
        textmenu1.classList.add('closed')
        textmenu7.classList.add('closed')
        textmenu9.classList.add('closed')
        textmenu10.classList.add('closed')
        textmenuc.classList.add('closed')
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