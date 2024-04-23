document.addEventListener('DOMContentLoaded', function() {

    modal = document.querySelector(".modal-container");
    openModalBtn = document.querySelector("#create-btn");
    closeModalBtn = document.querySelector(".close");
    modaloverlay = document.querySelector(".modal-overlay");
    form = document.getElementById("task-form");


    openModalBtn.addEventListener("click", function() {
        if (modaloverlay.classList.contains("show")) {
            modal.classList.remove("show")
            modaloverlay.classList.remove("show")
        } else {
            modal.classList.add("show")
            modaloverlay.classList.add("show")
        }
    });

    modaloverlay.addEventListener("click", function() {
        modal.classList.remove("show")
        modaloverlay.classList.remove("show")
        alert("Are you sure you want to leave this page? you have unsaved changes!")
        form.reset();
    });

    closeModalBtn.addEventListener("click", function () {
        if (modaloverlay.classList.contains("show")) {
            modal.classList.remove("show")
            modaloverlay.classList.remove("show")
            

            form.reset();
        }
    })

});







