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

        } else {
            modal.classList.add("show");
            modalOverlay.classList.add("show");
            //modalen finns fortfarande i backgrunden (osynlig)

        }
    });

    modalOverlay.addEventListener("click", function () {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        //modalen finns fortfarande i backgrunden (osynlig)
        //modal.style.display = "none";
        //modalOverlay.style.display = "none";
        //alert("Are you sure you want to leave this page? you have unsaved changes!")
        form.reset();
    });

    closeModalBtn.addEventListener("click", function () {
        if (modalOverlay.classList.contains("show")) {
            modal.classList.remove("show");
            modalOverlay.classList.remove("show");

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
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'task_id=' + encodeURIComponent(taskId)
        })
        
        .then(response => {
            if(!response.ok) {
                //ge ett felmeddelande om begäran inte lyckades
                console.error("Failed to delete task");

                //alert("Failed to delete task. Please try again later.");
                
            } 

            //I annat fall (om svaret lyckas) hämtar hanteraren svaret
            var row = document.querySelector('[data-task-id="' + taskId + '"]').closest('tr');

            // Ta bort motsvarande rad från tabellen
            row.remove();

        })

        .catch((error) => {
            console.error('Error', error);
            poemDisplay.textContent =document.createTextNode('Could not fetch verse: ' + error);

            //alert("An error occurred while deleting the task.");
        });

    };

    //Funktionen nedan sorterar tabellen 

    table_headings = document.querySelectorAll('thead th');
    table_rows = document.querySelectorAll('tbody tr')

    table_headings.forEach((head, i) => {
        if (i !== 1) {
            let sort_asc = true;

            head.onclick = () => {
                table_headings.forEach(h => {
                
                    h.classList.remove('active', 'asc');
                    if (h.querySelector('span.icon-arrow')) {
                        h.querySelector('span.icon-arrow').style.transform = "rotate(0deg)";
                    }
                });

                head.classList.add('active');

                if(head.querySelector('span.icon-arrow')) {
                    head.classList.toggle('asc', sort_asc);
                    head.querySelector('span.icon-arrow').style.transform = sort_asc ? "rotate(180deg)" : "rotate(0deg)";

                }

                sort_asc = !sort_asc;

                document.querySelectorAll('td').forEach(td => td.classList.remove('active'));
            
                table_rows.forEach(row => {
                    row.querySelectorAll('td')[i].classList.add('active');
                });
    
                sortTable(i, sort_asc);
            };

        }
            
    });

    function sortTable(column, sort_asc) {
        [...table_rows].sort((a, b) => {
            let first_row = a.querySelectorAll('td')[column].innerText.toLowerCase(),
                second_row = b.querySelectorAll('td') [column].innerText.toLowerCase();

            return sort_asc ? (first_row < second_row ? -1 : 1) : (first_row < second_row ? 1 : -1);

        })

        .forEach(sorted_row => document.querySelector('tbody').appendChild(sorted_row));
        
    };


    //funktion som gör data i tabellen redigerbar och sparar det nya värdet i databasen

    document.querySelectorAll('.editable-cell').forEach(function(cell) {
        cell.addEventListener('blur', function() {
            var taskId = this.dataset.taskId;
            var  newContent = this.textContent.trim();
            var cellType = this.getAttribute('data-cell');

            updateTask(taskId, cellType, newContent);
        });

    });

    //function som skickar ny data till bottle som sparar det i databasen
    function updateTask(taskId, cellType, newContent) {
        fetch('/update_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'task_id=' + encodeURIComponent(taskId) + '&cell_type=' + encodeURIComponent(cellType) + '&new_content=' + encodeURIComponent(newContent)
        })
        
        .then(response => {
            if(!response.ok) {
                //ge ett felmeddelande om begäran inte lyckades
                console.error("Failed to update task");

                //alert("Failed to delete task. Please try again later.");
                
            } 

            //I annat fall (om svaret lyckas) hämtar hanteraren svaret
            var cell = document.querySelector('[data-task-id="' + taskId + '"]');

            cell.contentEditable = false;

        })

        .catch((error) => {
            console.error('Error', error);

            alert("An error occurred while updating the task:" + error.message);
        });

    }
     
  
});







