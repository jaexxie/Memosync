open_popup_btn = document.querySelector('.open_popup_btn')
popup_container = document.querySelector('.popup_container')

// create to-do list
open_popup_btn_1 = document.querySelector('#open_popup_btn_1')
popup_container_1 = document.querySelector('#popup_container_1')
popup_background_1 = document.querySelector('#popup_background_1')

open_popup_btn_1.addEventListener('click', function () {
    popup_container_1.classList.add('show')
    popup_background_1.classList.add('show')
})

popup_background_1.addEventListener('click', function () {
    popup_container_1.classList.remove('show')
    popup_background_1.classList.remove('show')
})

// add new task
open_popup_btn_2 = document.querySelector('#open_popup_btn_2')
popup_container_2 = document.querySelector('#popup_container_2')
popup_background_2 = document.querySelector('#popup_background_2')

open_popup_btn_2.addEventListener('click', function () {
    popup_container_2.classList.add('show')
    popup_background_2.classList.add('show')
})

popup_background_2.addEventListener('click', function () {
    popup_container_2.classList.remove('show')
    popup_background_2.classList.remove('show')
})

// checkbox strikthrough
taskCheckboxes = document.querySelectorAll('.task_checkbox');

taskCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        this.parentNode.classList.toggle('completed');
    });
});

// delete todo
deleteButtons = document.querySelectorAll('.delete_todo');

deleteButtons.forEach((button) => {
    button.addEventListener('click', (event) => {
        event.preventDefault();

        toDoListId = button.id;

        fetch(`/delete_to_do_list/${toDoListId}`, {
            method: 'DELETE',
        })
            .then((response) => {
                if (response !== 404) { // Ändra tillbaka till response.ok när ni har löst att API:et returnerar 200 eller 201
                    console.log('To-do list deleted successfully.');
                    event.target.parentElement.parentElement.remove();
                } else {
                    console.error('Failed to delete the to-do list.');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });

    //funktion som sparar checkade element i listan

    checkboxes = document.querySelectorAll('.task_checkbox');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function() {
            var taskId = this.value;
            var isChecked = this.checked;

            fetch('/update_task_status', {
                method: 'POST',
                headers: {
                    'content-type': 'application/x-www-form-urlencoded'
                },
                body: 'task_id=' + encodeURIComponent(taskId) + '&checked=' + isChecked
            })

            .then(response => {
                if(!response.ok) {
                    console.error("Failed to update task status");
                }
            })
            .catch(error => {
                console.error('Error', error);
            });
        })
    })
});