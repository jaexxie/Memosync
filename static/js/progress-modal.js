
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector(".modal-container");
    const openModalBtn = document.getElementById("create-btn");
    const closeModalBtn = document.querySelector(".close");

    //Open modal when create-btn i clicked 
    const openModal = () => {
        modal.style.display = "block";
    }

    //close modal when close btn is clicked
    const closeModal = () => {
        modal.style.display = "none";
    }

    openModalBtn.addEventListener("click", openModal);

    closeModalBtn.addEventListener("click", closeModal);

    // Close modal when the Esc key is pressed
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && modal.style.display !== "none") {
        closeModal();
        }
    });


});
