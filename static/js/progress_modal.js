document.addEventListener('DOMContentLoaded', function () {

    modal = document.querySelector(".modal-container");
    openModalBtn = document.querySelector("#create-btn");
    closeModalBtn = document.querySelector(".close");
    modalOverlay = document.querySelector(".modal-overlay");
    form = document.getElementById("task-form");


    openModalBtn.addEventListener("click", function () {
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

    modalOverlay.addEventListener("click", function () {
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
    var statusForms = document.querySelectorAll(".status-update-form");

    //loopa genom varje select alternativ
    statusForms.forEach(function (form) {
        
        var selectElement = form.querySelector(".status-selector")
        
        //uppdatera backgrundsfärgen när select värde ändras
        selectElement.addEventListener("change", function () {
            form.submit();
        });
        
        //ge backgrundsfärgen baserad på select
        updateBackgroundColor(selectElement);
    })

    function updateBackgroundColor(select) {
        var selectedOption = select.value;
        var backgroundColor;

        //if (selectedOption === "not_started") {
        // backgroundColor = "#FFA07A"; } else if ...

        switch (selectedOption) {
            case "not_started":
                backgroundColor = "#cf7a74";
                break;
            case "in_progress":
                backgroundColor = "#f0eeb1";
                break;
            case "completed":
                backgroundColor = "#db95bc";
                break;
            default:
                backgroundColor = "#f8f8f8";
        }

        select.style.backgroundColor = backgroundColor;
    };


    //funktion som raderar task (uppgifter) från databasen
    //välj alla delete-task-btn
    document.querySelectorAll('.delete-task-btn').forEach(button => {
        // Lägg till händelselyssnare för varje raderingsknapp
        button.addEventListener("click", function () {
            var taskId = this.dataset.taskId;
            deleteTask(taskId);
        });
    });

    function deleteTask(taskId) {
        fetch('/delete_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded' // Set content type to form data
            },
            body: 'task_id=' + encodeURIComponent(taskId) // Encode task ID as form data
        })
        
        .then(response => {
            if(response.ok) {

                var row = document.querySelector('[data-task-id="' + taskId + '"]').closest('tr');

                // Ta bort motsvarande rad från tabellen
                row.remove();
                location.reload();
            } else {
                console.error("Failed to delete task");
            }
        })

        .catch(error => {
            console.error('Error', error);
        });


    }
            
        


});







