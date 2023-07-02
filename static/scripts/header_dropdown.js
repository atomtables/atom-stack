function dropdownOnClick() {
    document.querySelectorAll('div.header-button.title').forEach(a => {
        a.classList.toggle('header-button-active')
    });
    document.querySelectorAll('.dropdown-content, .padding-space.to-disappear, .right-selectors').forEach(a => {
        if (a.classList.contains('show')) {
            a.classList.add('hide');
            a.classList.remove('show');
        } else {
            a.classList.add('show');
            a.classList.remove('hide');
        }
    });
}