const userInfo = document.getElementById("userInfo");
const userInfoDropdown = document.getElementById("userInfoDropdown");
document.querySelectorAll(".dropdown-content").forEach(a => a.style.height = 'auto');
document.querySelectorAll(".dropdown-link").forEach(a => a.style.height = 'auto');
document.querySelectorAll(".dropdown-link").forEach(a => a.style.display = 'block');
userInfoDropdown.style.width = userInfo.offsetWidth + "px";
userInfoDropdown.style.left = `${userInfo.getBoundingClientRect().left - userInfoDropdown.getBoundingClientRect().left}px`;
userInfoDropdown.style.top = `${userInfo.getBoundingClientRect().y + userInfo.getBoundingClientRect().height - userInfoDropdown.getBoundingClientRect().y}px`
const userInfoDropdownHeight = userInfoDropdown.getBoundingClientRect().height;
const userInfoDropdownLinkHeight = document.querySelector("#primary-link").getBoundingClientRect().height - 24;
document.querySelectorAll(".dropdown-content").forEach(a => a.style.height = '');
document.querySelectorAll(".dropdown-link").forEach(a => a.style.height = '');
document.querySelectorAll(".dropdown-link").forEach(a => a.style.display = '');
document.querySelectorAll(".dropdown-content").forEach(a => a.style.setProperty("--dropdown-content-height", `${userInfoDropdownHeight}px`));
document.querySelectorAll(".dropdown-link").forEach(a => a.style.setProperty("--dropdown-link-height", `${userInfoDropdownLinkHeight}px`));

function dropdownOnClick() {
    document.querySelectorAll(".dropdown-content").forEach(a => {
        if (a.classList.contains('show')) {
            document.querySelectorAll(".dropdown-link").forEach(a => a.classList.remove('show'));
            document.querySelectorAll(".dropdown-content").forEach(a => a.classList.remove('show'));
            document.querySelectorAll(".dropdown-link").forEach(a => a.style.setProperty("animation", "downToUpLink 0.5s forwards"));
            document.querySelectorAll(".dropdown-content").forEach(a => a.style.setProperty("animation", "downToUpContent 0.5s forwards"));
            setTimeout(function () {
                document.querySelectorAll(".dropdown-link").forEach(a => a.style.setProperty("display", "none"));
            }, 500)
        } else {
            //setTimeout(function () {
                document.querySelectorAll(".dropdown-link").forEach(a => a.style.setProperty("display", "block"));
            //}, 500)
            document.querySelectorAll(".dropdown-link").forEach(a => a.style.setProperty("animation", ""));
            document.querySelectorAll(".dropdown-content").forEach(a => a.style.setProperty("animation", ""));
            document.querySelectorAll(".dropdown-content").forEach(a => a.classList.add('show'));
            document.querySelectorAll(".dropdown-link").forEach(a => a.classList.add('show'));
        }
    })
}