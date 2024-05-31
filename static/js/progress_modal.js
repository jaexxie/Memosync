document.addEventListener('DOMContentLoaded', function () {
    // Hämtar alla element som hanterar modalen
    modal = document.querySelector(".modal-container");
    openModalBtn = document.querySelector("#create-btn");
    closeModalBtn = document.querySelector(".close");
    modalOverlay = document.querySelector(".modal-overlay");
    form = document.getElementById("task-form");

    // Öppnar modalen när "create-btn" klickas
    openModalBtn.addEventListener("click", function () {
        modal.classList.add("show");
        modalOverlay.classList.add("show");
    });

    //Stänger modalen när "overlay" klickas och återställer formuläret 
    modalOverlay.addEventListener("click", function () {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        form.reset();
    });

    //Stänger modalen när "close" knappen klickas, formuläret nollställs
    closeModalBtn.addEventListener("click", function () {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        form.reset();
    });

    //Funktion som uppdaterar backgrundsfärgen på select-elementen baserat på dess värde
    var statusForms = document.querySelectorAll(".status-update-form");

    //loopa genom varje status formulär och lägger till eventlistener 
    //Som uppdaterar backgrundsfärgen vid ändring
    statusForms.forEach(function (form) {
        var selectElement = form.querySelector(".status-selector")
        //uppdatera backgrundsfärgen när select värde ändras
        selectElement.addEventListener("change", function () {
            form.submit(); //Formuläret skickas när värdet ändras
        });

        //ge backgrundsfärgen baserad på select
        updateBackgroundColor(selectElement);
    })

    // Funktion som ger backgrundsfärg baserat på valt statusvärde
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
    //hämta alla delete-task-btn
    document.querySelectorAll('.delete-task-btn').forEach(button => {
        // Händelselyssnare för varje raderingsknapp
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
            if (!response.ok) {
                //ge ett felmeddelande om begäran inte lyckades
                console.error("Failed to delete task");
                //alert("Failed to delete task. Please try again later.");
            } else {
                //I annat fall (om svaret lyckas) hämtar hanteraren svaret
                var row = document.querySelector('[data-task-id="' + taskId + '"]').closest('tr');
                row.remove(); // Ta bort motsvarande rad från tabellen
            }

        })
        .catch((error) => {
            console.error('Error', error);
            alert("An error occurred while deleting the task.");
        });
    };

    //Funktionen nedan sorterar tabellen 
    const tableHeadings = document.querySelectorAll('thead th');
    let tableRows = Array.from(document.querySelectorAll('tbody tr'));

    tableHeadings.forEach((head, i) => {
        //Excludera beskrivningskolumnen från sortering "(i !== 1)"
        if (i !== 1) {
            //Hålla reda på sorteringen (stigande/fallande)
            let sortAsc = true;

            head.onclick = () => {
                // ta bort "active" och "asc" klasser från alla kloumnrubriker
                tableHeadings.forEach(h => {
                    h.classList.remove('active', 'asc');
                    //återställler pillens riktning
                    if (h.querySelector('span.icon-arrow')) {
                        h.querySelector('span.icon-arrow').style.transform = "rotate(0deg)";
                    }
                });

                //Klickad komlumnrubrik får klassen "active"
                head.classList.add('active');
                if (head.querySelector('span.icon-arrow')) {
                    head.classList.toggle('asc', sortAsc);
                    head.querySelector('span.icon-arrow').style.transform = sortAsc ? "rotate(180deg)" : "rotate(0deg)";
                }

                sortAsc = !sortAsc;
                document.querySelectorAll('td').forEach(td => td.classList.remove('active'));

                //Lägg till "active" klass till cellern i sorterade kolumnen
                tableRows.forEach(row => {
                    row.querySelectorAll('td')[i].classList.add('active');
                });

                //Anropa funktion
                sortTable(i, sortAsc);
            };
        }
    });

    function sortTable(column, sortAsc) {
        tableRows.sort((a, b) => {
            let firstRow = a.querySelectorAll('td')[column].innerText.toLowerCase();
            let secondRow = b.querySelectorAll('td')[column].innerText.toLowerCase();

            //sortera datum kolumner 
            if(column === 2) {
                firstRow = new Date(firstRow);
                secondRow = new Date(secondRow);
                return sortAsc ? firstRow - secondRow : secondRow - firstRow;
            } else if (column === 3) {
                // Sortera status kolumner 
                const statusOrder = ["not_started", "in_progress", "completed"];
                firstRow = statusOrder.indexOf(a.querySelectorAll("td")[column].querySelector("select").value);
                secondRow = statusOrder.indexOf(b.querySelectorAll("td")[column].querySelector("select").value);
                return sortAsc ? firstRow - secondRow : secondRow - firstRow;
            } else {
                //Sortera text kolumner             
                return sortAsc ? (firstRow < secondRow ? -1 : 1) : (firstRow < secondRow ? 1 : -1);
            }
        });

        const tbody = document.querySelector("tbody");
        tbody.innerHTML = '';
        tableRows.forEach(row => tbody.appendChild(row));    
    }

    //funktion som gör data i tabellen redigerbar och sparar det nya värdet i databasen
    document.querySelectorAll('.editable-cell').forEach(function (cell) {
        cell.addEventListener('blur', function () {
            var taskId = this.dataset.taskId;
            var newContent = this.textContent.trim();
            var cellType = this.getAttribute('data-cell');

            updateTask(taskId, cellType, newContent);
        });

    });

    //function som skickar ny data till servern för att sparar det i databasen
    function updateTask(taskId, cellType, newContent) {
        fetch('/update_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'task_id=' + encodeURIComponent(taskId) + '&cell_type=' + encodeURIComponent(cellType) + '&new_content=' + encodeURIComponent(newContent)
        })
        .then(response => {
            if (!response.ok) {
                //ge ett felmeddelande om begäran inte lyckades
                console.error("Failed to update task");
                alert("Failed to delete task. Please try again later.");
            }
        })
        .catch((error) => {
            console.error('Error', error);
            alert("An error occurred while updating the task:" + error.message);
        });
    }

    //Nedan kod är för Bootstrap popovers 
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        var popover = new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover'
        });

        //Dölj popover när elementet klickas  
        popoverTriggerEl.addEventListener('click', function () {
            popover.hide();
        });
    });
});