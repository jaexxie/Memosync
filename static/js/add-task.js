document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector(".modal-container");
    const form = document.querySelector(".modal-body form");
    const createBtn = document.querySelector(".add-task-btn");

    // Handle form submission when modal-create-btn is clicked
    createBtn.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent form submission
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
                <form action="#">
                    <select name="status" id="status">
                        <option value="choose_status"  disabled>Choose Status</option>
                        <option value="not_started" selected>Not Started</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                    </select>
                </form>
            </td>
        `;
        tableBody.appendChild(newRow);

        // Close the modal after adding the task
        closeModal();
    });
});
