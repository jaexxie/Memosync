document.addEventListener('DOMContentLoaded', function() {

    open_popup_btn = document.querySelector('.open_popup_btn')
    popup_container = document.querySelector('.popup_container')

    // create to-do list
    open_popup_btn_1 = document.querySelector('#open_popup_btn_1')
    popup_container_1 = document.querySelector('#popup_container_1')
    popup_background_1 = document.querySelector('#popup_background_1')
    closeBtn_1 = document.querySelector(".close_1");

    open_popup_btn_1.addEventListener('click', function () {
        popup_container_1.classList.add('show')
        popup_background_1.classList.add('show')
    });

    popup_background_1.addEventListener('click', function () {
        popup_container_1.classList.remove('show')
        popup_background_1.classList.remove('show')
    });

    closeBtn_1.addEventListener('click', function() {
        popup_container_1.classList.remove('show');
        popup_background_1.classList.remove('show');

    });

    // add new task
    open_popup_btn_2 = document.querySelector('#open_popup_btn_2')
    popup_container_2 = document.querySelector('#popup_container_2')
    popup_background_2 = document.querySelector('#popup_background_2')
    closeBtn_2 = document.querySelector(".close_2");


    open_popup_btn_2.addEventListener('click', function () {
        popup_container_2.classList.add('show')
        popup_background_2.classList.add('show')
    })

    popup_background_2.addEventListener('click', function () {
        popup_container_2.classList.remove('show')
        popup_background_2.classList.remove('show')
    })

    closeBtn_2.addEventListener('click', function() {
        popup_container_2.classList.remove('show');
        popup_background_2.classList.remove('show');

    });



    //funktion som raderar task todolist med alla tillhörande uppgifter från databasen
    //hämta alla delete-list-btn
    document.querySelectorAll('.delete_list_btn').forEach(button => {
        // Lägg till händelselyssnare för varje raderingsknapp
        button.addEventListener("click", function () {
            toDoListId = this.dataset.taskId;

            var buttonElement = this;

            deleteToDoList(toDoListId, buttonElement);
        });
    });

    //Delete todo list
    function deleteToDoList(toDoListId, buttonElement) {
        fetch('/delete_to_do_list', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'to_do_list_id=' + encodeURIComponent(toDoListId)
        })
        
        .then(response => {
            if(!response.ok) {
                //ge ett felmeddelande om begäran inte lyckades
                console.error("Failed to delete List");

                //alert("Failed to delete task. Please try again later.");
                
            }

            var parentElement = buttonElement.closest(".to_do_lists");
            if(parentElement) {
                parentElement.remove();
            } else {
                console.error("List not found")
            }
            

        })

        .catch((error) => {
            console.error('Error', error);
            //poemDisplay.textContent =document.createTextNode('Could not fetch verse: ' + error);

            //alert("An error occurred while deleting the List.");
        });

    }

    //funktion som raderar task i todo_listan
    //det går att utöka den tidigare kod som raderar hela listan med alla task
    //separat funktion håller koden mer läsbar och underhållbar 
    document.querySelectorAll('.delete_todo_task_btn').forEach(taskbutton => {
        // Lägg till händelselyssnare för varje raderingsknapp
        taskbutton.addEventListener("click", function () {
             const taskId = this.dataset.taskId;

            deleteToDoTask(taskId, this.closest("label"));
        });
    });

    //Delete todo task 
    function deleteToDoTask(taskId, labelElement) {
        fetch('/delete_to_do_task', {
            method: 'DELETE',
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
                
            } else {
                //tar bort uppgiften från DOM
                labelElement.remove();
            }
            

        })

        .catch((error) => {
            console.error('Error', error);
            
        });

    };

    //funktion som sparar checkade element i listan
    checkboxes = document.querySelectorAll('.task_checkbox');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", function(event) {
            event.preventDefault();
            var taskId = this.dataset.taskId;
            var isChecked = this.checked;
            var span = event.target.nextElementSibling;

            fetch('/update_checkbox', {
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

            if (isChecked) {
                span.classList.add("checked")
            } else {
                span.classList.remove("checked")
            } 
            
        });
    });
});