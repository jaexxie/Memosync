document.addEventListener("DOMContentLoaded", function() {
    var btn = document.getElementsByClassName("create-btn")[0];
    var modal = document.querySelector(".modal-container"); // Use querySelector to select the modal container
    var span = document.getElementsByClassName("close")[0];

    // Check if the button element exists
    if (btn) {
        // Add event listener for click event
        btn.onclick = function() {
            modal.style.display = "block";
        }
    } else {
        console.error("Button element not found.");
    }

    // Rest of your code for modal functionality
});
