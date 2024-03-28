open_popup_btn = document.querySelector('#open_popup_btn')
popup_background = document.querySelector('.popup_background')
popup_container = document.querySelector('.popup_container')

open_popup_btn.addEventListener('click', function() {
    if (popup_background.classList.contains('show')) {
        popup_background.classList.remove('show')
        popup_container.classList.remove('show')
    } else {
        popup_background.classList.add('show')
        popup_container.classList.add('show')
    }
});

popup_background.addEventListener("click", function() {
    popup_background.classList.remove('show')
    popup_container.classList.remove('show')
});