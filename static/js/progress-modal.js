
const modal = document.querySelector(".modal-container");
const openModalBtn = document.getElementById("create-btn");
const closeModalBtn = document.querySelector(".close");
const modaloverlay = document.querySelector(".modal-overlay");


//Open modal when create-btn i clicked 
//const openModal = () => {
   // modal.classList.add('show');
   // modaloverlay.classList.add('show');
//}

openModalBtn.addEventListener('click', function () {
    modal.style.display = "block";
    modaloverlay.style.display = "block";
})

//close modal when close btn is clicked
closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
    modaloverlay.style.display = "none";
});

// Close modal when the Esc key is pressed
document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && modal.style.display !== "none") {
    closeModal();
    }
});

