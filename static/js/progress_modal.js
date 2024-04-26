document.addEventListener('DOMContentLoaded', function() {

    modal = document.querySelector(".modal-container");
    openModalBtn = document.querySelector("#create-btn");
    closeModalBtn = document.querySelector(".close");
    modalOverlay = document.querySelector(".modal-overlay");
    form = document.getElementById("task-form");


    openModalBtn.addEventListener("click", function() {
        if (modalOverlay.classList.contains("show")) {
            modal.classList.remove("show");
            modalOverlay.classList.remove("show");
            //modalen finns fortfarande i backgrunden (osynlig)
            modal.style.display = "none";
            modalOverlay.style.display = "none";
        } else {
            modal.classList.add("show");
            modalOverlay.classList.add("show");
            //modalen finns fortfarande i backgrunden (osynlig)
            modal.style.display = "block";
            modalOverlay.style.display = "block";
        }
    });

    modalOverlay.addEventListener("click", function() {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        //modalen finns fortfarande i backgrunden (osynlig)
        modal.style.display = "none";
        modalOverlay.style.display = "none";
        alert("Are you sure you want to leave this page? you have unsaved changes!")
        form.reset();
    });

    closeModalBtn.addEventListener("click", function () {
        if (modalOverlay.classList.contains("show")) {
            modal.classList.remove("show");
            modalOverlay.classList.remove("show");
            //lösningen funkar ej 
            modal.style.display = "none";
            modalOverlay.style.display = "none";
            
            form.reset();
        }
    });

    //Funktion som uppdaterar backgrundsfärgen på select (#status-col)
    var selects = document.querySelectorAll(".status-col");

    //loopa genom varje select element 

    selects.forEach(function (select) {
        //uppdatera backgrundsfärgen när select värde ändras
        select.addEventListener("change", function() {
            updateBackgroundColor(this);
        });
        
        updateBackgroundColor(select);
    })
    
    function updateBackgroundColor(select) {
        var selectedOption = select.value;
        var backgroundColor;

        //if (selectedOption === "not_started") {
           // backgroundColor = "#FFA07A"; } else if ...
        
        switch(selectedOption) {
            case "not_started":
                backgroundColor = "#FFA07A";
                break;
            case "in_progress":
                backgroundColor = "#FFFF99";
                break;
            case "completed":
                backgroundColor = "#90EE90";
                break;
            default:
                backgroundColor = "#f8f8f8";
        }

        select.style.backgroundColor = backgroundColor;
    };

        // Add an event listener to each select element
        document.querySelectorAll('.status-col').forEach(select => {
            select.addEventListener('change', function() {
                // Get the project ID from the select element's ID
                const projectId = this.id.split('-')[1];
                // Get the updated status value
                const status = this.value;
                // Send an AJAX request to update the status
                fetch('/update_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ projectId, status })
                })
                .then(response => {
                    // Handle the response if needed
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        });

    
});







