
const addTaskForm = document.querySelector(".modal-form-box form");
const addTaskBtn = document.querySelector(".add-task-btn");
const modal = document.querySelector(".modal-container");
const modaloverlay = document.getElementById("modal-overlay");

// Handle form submission when modal-create-btn is clicked
function addTask (e) {

    // Prevent form submission
    e.preventDefault();

    // Get form input values
    const task = document.getElementById("task").value;
    const description = document.getElementById("description").value;
    const deadlineDate = document.getElementById("deadline_date").value;

   
    // Add a new row to the progress table with the form values
    const tableBody = document.querySelector("#progress_container table tbody");
    
    const newRow = document.createElement("tr");

    newRow.innerHTML = `
        <td>${task}</td>
        <td>${description}</td>
        <td>${deadlineDate}</td>
        <td>
            <select class="status-select">
            <option  value="Choose status"  disabled>Choose Status</option>
            <option id="not-started" value="Not started" selected>Not Started</option>
            <option id="in-progress" value="In progress">In Progress</option>
            <option id="done" value="Done">Done</option>
            </select>
        </td>
    `;

    const selectStatus = newRow.querySelector(".status-select");
    // Lägg till händelselyssnare för att ändra bakgrundsfärg på select
    selectStatus.addEventListener("change", function() {
        
        // Om det valda alternativet är "Not started", ändra bakgrundsfärgen
        if (selectedValue === "Not started") {
            selectStatus.style.backgroundColor = "red"; // Ändra till önskad färg
        }
    });
    

    tableBody.appendChild(newRow);

    addTaskForm.reset();
    closeModal();

};

addTaskForm.addEventListener("submit", addTask);

//function that closes the modal (temporary and needs improvement)
function closeModal() {
    modal.style.display = "none"
    modaloverlay.style.display = "none"

}
