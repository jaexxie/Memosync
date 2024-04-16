//const modal = document.querySelector("#modal-container");
//const openModalBtn = document.querySelector(".create-btn");
//const closeModalBtn = document.querySelector(".close");

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector(".modal-container");
    const openModalBtn = document.getElementById("create-btn");
    const closeModalBtn = document.querySelector(".close");

    //Open modal when create-btn i clicked 
    openModalBtn.addEventListener("click", () => {
        modal.style.display = "block";
    });

    //close modal when close btn is clicked
    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";


    });

    //close modal even with clicking outside the modal
    document.addEventListener("click", function (e) {
        if(e.target === modal) {
            modal.style.display = "none";
        }
    });

    // Close modal when the Esc key is pressed
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && modal.style.display !== "none") {
        closeModal();
        }
    });
});
