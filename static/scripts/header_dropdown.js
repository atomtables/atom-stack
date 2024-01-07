function dropdownOnClick() {
    document.querySelector('#userInfo').classList.toggle('header-button-active')
    document.querySelectorAll('.dropdown-content, .padding-space.to-disappear, .right-selectors').forEach(a => {
        if (a.classList.contains('show')) {
            a.classList.add('hide');
            a.classList.remove('show');
            setTimeout(() => {
                a.classlist.remove('hide')
            }, 500)
        } else {
            a.classList.add('show');
            a.classList.remove('hide');
        }
    });
    if (document.querySelector('#userInfo').classList.contains('header-button-active')) {
        // if width 900px or less, hide header buttons
        if (window.innerWidth <= 900) {
            document.querySelectorAll('.mobile-hide').forEach(a => {
                a.style.display = "none";
            })
        }
    } else {
        // if width 900px or less, show header buttons. else keep hiding them
        if (window.innerWidth <= 610) {
            document.querySelectorAll('.mobile-hide').forEach(a => {
                a.style.display = "none";
            })
        } else if (window.innerWidth <= 900) {
            document.querySelectorAll('.mobile-hide').forEach(a => {
                a.style.display = "initial";
            })
        }
    }
    // if width higher than 900px, show header buttons
    if (window.innerWidth > 900) {
        document.querySelectorAll('.header-button').forEach(a => {
            a.style.display = "initial";
        })
    }
}

if (document.querySelector('.error, .warning, .success, .info')) {
    setTimeout(() => {
        document.querySelectorAll('.error, .warning, .success, .info').forEach(a => {
            a.style.display = 'none';
        })
        document.querySelectorAll('.dropdown-content, .padding-space.to-disappear, .right-selectors').forEach(a => {
            a.classList.remove('hide');
            a.classList.add('hide');
        })
    }, 7500)
}
