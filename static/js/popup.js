open_popup_btn = document.querySelector('#open_popup_btn')
popup_container = document.querySelector('.popup_container')

// open_popup_btn.addEventListener('click', function () {
//     if (popup_container.classList.contains('show')) {
//         popup_container.classList.remove('show')
//     } else {
//         popup_container.classList.add('show')
//     }
// });

// popup_container.addEventListener("click", function () {
//     popup_container.classList.remove('show')
// });

open_popup_btn = document.querySelector('#open_popup_btn')
popup_container = document.querySelector('.popup_container')
const dialog = document.getElementById("dialog")
dialog.onclick = (event) => { event.target.className = "hidden_dialog"; console.log(event.target.className) }
open_popup_btn.addEventListener('click', function () {
    // if (popup_container.classList.contains('show')) {
    //     popup_container.classList.remove('show')
    // } else {
    // popup_container.classList.add('show')
    if (dialog.className === "hidden_dialog") dialog.className = "shown_dialog"; return;
    if (dialog.className === "shown_dialog") dialog.className = "hidden_dialog"; return;
    // }
});
