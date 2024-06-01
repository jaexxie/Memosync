document.addEventListener('DOMContentLoaded', function () {
    // retrieves all elements that handle the modal
    modal = document.querySelector(".modal-container");
    openModalBtn = document.querySelector("#create-btn");
    closeModalBtn = document.querySelector(".close");
    modalOverlay = document.querySelector(".modal-overlay");
    form = document.getElementById("task-form");

    // opens the modal when 'create-btn' is clicked
    openModalBtn.addEventListener("click", function () {
        modal.classList.add("show");
        modalOverlay.classList.add("show");
    });

    // closes the modal when 'overlay' is clicked and resets the form
    modalOverlay.addEventListener("click", function () {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        form.reset();
    });

    // closes the modal when 'close' buttonis clicked and resets the form
    closeModalBtn.addEventListener("click", function () {
        modal.classList.remove("show");
        modalOverlay.classList.remove("show");
        form.reset();
    });

    // function that updates teh background colour of the select elements based on their value
    var statusForms = document.querySelectorAll(".status-update-form");

    // loops through each status form and adds an event listener
    // that updates the background colour when the value changes
    statusForms.forEach(function (form) {
        var selectElement = form.querySelector(".status-selector")
        // updates the background colour when the select value changes
        selectElement.addEventListener("change", function () {
            form.submit(); // the form is submitted when the value changes
        });

        // sets the background colour based on the select element
        updateBackgroundColor(selectElement);
    })

    // function that sets background colour based on selected status value
    function updateBackgroundColor(select) {
        var selectedOption = select.value;
        var backgroundColor;
        // determines background colour based on selected status value
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

    // function that deletes tasks from the database
    // gets all delete-task-btn element
    document.querySelectorAll('.delete-task-btn').forEach(button => {
        // event listener for each delete button
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
                    // provides an error message if the request fails
                    console.error("Failed to delete task");
                    // alert("Failed to delete task. Please try again later.");
                } else {
                    // otherwise (if the response is successful), handle the response
                    var row = document.querySelector('[data-task-id="' + taskId + '"]').closest('tr');
                    row.remove(); // remove the corresponding row
                }

            })
            .catch((error) => {
                console.error('Error', error);
                alert("An error occurred while deleting the task.");
            });
    };

    // the function below sorts the table
    const tableHeadings = document.querySelectorAll('thead th');
    let tableRows = Array.from(document.querySelectorAll('tbody tr'));

    tableHeadings.forEach((head, i) => {
        // excludes the description column from sorting "(i !== 1)"
        if (i !== 1) {
            // keeps track of the sorting (ascending/descending)
            let sortAsc = true;

            head.onclick = () => {
                // remove 'active' and 'asc' classes from all column headings
                tableHeadings.forEach(h => {
                    h.classList.remove('active', 'asc');
                    // resets the arrows direction
                    if (h.querySelector('span.icon-arrow')) {
                        h.querySelector('span.icon-arrow').style.transform = "rotate(0deg)";
                    }
                });

                // the clicked column heading gets the 'active' class
                head.classList.add('active');
                if (head.querySelector('span.icon-arrow')) {
                    head.classList.toggle('asc', sortAsc);
                    head.querySelector('span.icon-arrow').style.transform = sortAsc ? "rotate(180deg)" : "rotate(0deg)";
                }

                sortAsc = !sortAsc;
                document.querySelectorAll('td').forEach(td => td.classList.remove('active'));

                // add the 'active' class to cells in the sorted column
                tableRows.forEach(row => {
                    row.querySelectorAll('td')[i].classList.add('active');
                });

                // calls function
                sortTable(i, sortAsc);
            };
        }
    });

    function sortTable(column, sortAsc) {
        tableRows.sort((a, b) => {
            let firstRow = a.querySelectorAll('td')[column].innerText.toLowerCase();
            let secondRow = b.querySelectorAll('td')[column].innerText.toLowerCase();

            // sorts date columns
            if (column === 2) {
                firstRow = new Date(firstRow);
                secondRow = new Date(secondRow);
                return sortAsc ? firstRow - secondRow : secondRow - firstRow;
            } else if (column === 3) {
                // sorts status columns
                const statusOrder = ["not_started", "in_progress", "completed"];
                firstRow = statusOrder.indexOf(a.querySelectorAll("td")[column].querySelector("select").value);
                secondRow = statusOrder.indexOf(b.querySelectorAll("td")[column].querySelector("select").value);
                return sortAsc ? firstRow - secondRow : secondRow - firstRow;
            } else {
                // sorts text columns        
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

    // function to send new data to the server to save it in the database
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
                    // provides an error message if the request fails
                    console.error("Failed to update task");
                    alert("Failed to delete task. Please try again later.");
                }
            })
            .catch((error) => {
                console.error('Error', error);
                alert("An error occurred while updating the task:" + error.message);
            });
    }

    // the code below is for Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.forEach(function (popoverTriggerEl) {
        var popover = new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover'
        });

        // hide popover when the element is clicked
        popoverTriggerEl.addEventListener('click', function () {
            popover.hide();
        });
    });
});