hamburger_btn = document.querySelector('#hamburger_btn')
header_slide_in_background = document.querySelector('.header_slide_in_background')
header_slide_in_container = document.querySelector('.header_slide_in_container')

hamburger_btn.addEventListener("click", function() {
    if (header_slide_in_background.classList.contains('show')) {
        header_slide_in_background.classList.remove('show')
        header_slide_in_container.classList.remove('show')
    } else {
        header_slide_in_background.classList.add('show')
        header_slide_in_container.classList.add('show')
    }
    print('awdawdaw')
});

header_slide_in_background.addEventListener("click", function() {
    header_slide_in_background.classList.remove('show')
    header_slide_in_container.classList.remove('show')
});
