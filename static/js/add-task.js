
const addTaskForm = document.querySelector(".modal-body form");
const addTaskBtn = document.querySelector(".add-task-btn");
const modal = document.querySelector(".modal-container");

// Handle form submission when modal-create-btn is clicked
function addTask (e) {

    // Prevent form submission
    e.preventDefault();

    // Get form input values
    const task = document.getElementById("task").value;
    const description = document.getElementById("description").value;
    const deadlineDate = document.getElementById("deadline_date").value;
    const status = document.getElementById("status").value;
   
    // Add a new row to the progress table with the form values
    const tableBody = document.querySelector("#progress_container table tbody");
    
    const newRow = document.createElement("tr");

    newRow.innerHTML = `
        <td>${task}</td>
        <td>${description}</td>
        <td>${deadlineDate}</td>
        <td>${status}</td>
    `;
    tableBody.appendChild(newRow);

    addTaskForm.reset();
    closeModal();

};
 addTaskForm.addEventListener("click", function(event) {
    if (event.target.tagName === "INPUT") {
        event.preventDefault();
    }

});

addTaskForm.addEventListener("submit", addTask);

//function that closes the modal (temporary and needs improvement)
function closeModal() {
    modal.style.display = "none"
}
