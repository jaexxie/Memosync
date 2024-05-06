#from crypt import methods
from bottle import route, run, template, static_file, request, redirect, response, delete
import json
import os
from db import make_db_connection
import requests

@route('/')
def index():
    '''
    Route for the home page.

    If a user is already logged in, the user is redirected to the
    overiew page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        # user is not logged in and remains on the home page
        return template('index')

@route('/register')
def register():
    '''
    Route for the registration page.

    If a user is already logged in, the user is redirected to the
    overview page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    
    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        # user is not logged in and remains on the registstation page
        return template('register', message=None)

@route('/register/<message>')
def register(message):
    '''
    Route for regristration page with a message parameter.

    If a user is already logged in, the user is redirected to the
    overview page.
    '''
    
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        # user is not logged in and remains on the registstation page with the given message
        return template('register', message=message)

@route('/register/add/user', method=['post'])
def add_user():
    '''
    Route to add new user to the database.

    This function is called when a user submits the registration form.
    It retrieves user information from the same form, checks for 
    existing users with the same email and adds the new user to the
    database if the email does not already exist.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # checks that the request method is POST
            if request.method == 'POST':
                # retrieves form data submitted by the user
                first_name = request.forms.get('first_name')
                last_name = request.forms.get('last_name')
                email = request.forms.get('email')
                password = request.forms.get('password')

                # ensures the email does not already exist in the database
                cursor.execute('SELECT * FROM user_info WHERE email=%s', (email,))
                does_mail_already_exist = cursor.fetchall()
                
                if does_mail_already_exist:
                    # if email arlreayd exists, redirect with the message
                    return redirect('/register/Email already exists')

                # inserts the new user into the ddatabase
                cursor.execute('INSERT INTO user_info (name, lastname, email, password) VALUES (%s, %s, %s, %s)', (first_name, last_name, email, password))
                # commits the transaction
                db.commit()

                # redirects the user to the login page after successful registration
                return redirect('/login')
        finally:
            # close database connection
            cursor.close()
            db.close()

@route('/login', method=['GET', 'POST'])
def login():
    '''
    Route for hte login page.

    Checks if a user is already logged in. If the login is a GET
    request, it render the login page. If the login is a POST request,
    it verifies the user's login info.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # checks that the request method is POST
            if request.method == 'POST':

                # retrieves the email and password from the form
                email = request.forms.get('email')
                password = request.forms.get('password')

                # checks if the user exists with the given email and password
                cursor.execute('select * from user_info where email=%s and password=%s', (email, password))
                user = cursor.fetchone()

                if user:
                    # if the user exists, sets a cookie indicating they are logged in
                    response.set_cookie('loggedIn', str(user[0]))

                    # redirects the user to the overview page after successful login
                    return redirect('/overview')
                else:
                    return template('login', email_or_password_wrong=True)
            else:
                # renders the login page without error
                return template('login', email_or_password_wrong=False)
        finally:
            # close database connection
            cursor.close()
            db.close()

@route('/overview')
def overview():
    '''
    Route for the overview page.

    Checks if a user is already logged in. If the user is logged in,
    to-do lists and progess bar data from the database. If user is not
    logged in, user is redirected to the home page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # fetches all to-do lists for the logged-in user
            cursor.execute('SELECT * FROM to_do_list WHERE user_id = %s', (logged_in_cookie))
            todos = cursor.fetchall()

            # fetch progress bar data for the logged-in user
            cursor.execute("SELECT id, project, description, spb_date, status FROM progress_bar WHERE user_id = %s;", (logged_in_cookie,))
            pbs = cursor.fetchall()

            # returns the overview page with the to-do lists, progress bar data, and user info
            return template('overview', pbs=pbs, todos=todos, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route('/update/user/info', method=['GET', 'POST'])
def update_user_info():
    '''
    Route to update user information.

    Updates the user's personal information in the database. If the
    user is not logged in, the user is redirected to the home page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves the user information from the form
            first_name = request.forms.get('first_name')
            last_name = request.forms.get('last_name')
            email = request.forms.get('email')
            password = request.forms.get('password')
            image = request.files.get('pic')

            if image:
                # save the image to the specified directory
                filename = image.filename
                filepath = os.path.join('static/pic/user_profile_pictures', filename)
                image.save(filepath)

                # update the user's profile picture in the database
                cursor.execute("UPDATE memosync.user_info SET profile_picture = %s WHERE id = %s", (filename, logged_in_cookie))
                db.commit()

            # update the user's information in the database
            cursor.execute("UPDATE memosync.user_info SER name = %s, lastname = %s, email = %s, password = %s WHERE id = %s", (first_name, last_name, email, password, logged_in_cookie))
            db.commit()
            
            # redirects the user back to the referring page after a successful update
            return redirect(request.get_header('Referer'))
        except:
            # handle any errors by redirecting back to the referring page
            return redirect(request.get_header('Referer'))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

def get_user_info(id, cursor):
    '''
    Retrieves the user information based on the given user ID. Returns
    first tow that matches the user ID from the database.
    '''
    # fetches the user information by the ID 
    cursor.execute('SELECT * FROM user_info WHERE id = %s', (id))
    # returns the first row from the result set
    return cursor.fetchone()

@route('/logout', method=['GET', 'POST'])
def logout():
    '''
    Route for logging out users

    If the user is logged in, it clears the 'loggedIn' cookie to log
    the user out and redirects them to the home page. If the user is
    not logged in, it still redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        response.set_cookie('loggedIn', '', expires=0)
        # redirects to the home page after logging out
        return redirect('/')
    else:
        # if not logged in, redirects to the home page
        return redirect('/')

@route('/to_do_list')
def to_do_list():
    '''
    Route for the to-do list page.

    Retrieves the to-do lists and tasks for the logged-in user from
    the database. If the user is not logged in, the user redirects
    them to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # fetches all to-do lists for the logged-in user
            cursor.execute('SELECT * FROM to_do_list WHERE user_id = %s', (logged_in_cookie))
            category = cursor.fetchall()

            # fetches all tasks for the logged-in user
            cursor.execute('SELECT * from to_do_lists_task where user_id = %s', (logged_in_cookie))
            tasks = cursor.fetchall()

            # renders the 'to_do_list' template with the retrieved data
            return template('to_do_list', category=category, tasks=tasks, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route('/create_to_do_list', method='POST')
def create_to_do_list():
    '''
    Route for creating a new to-do lsit.

    Retrieves the to-do list title and description from the form data,
    inserts the new to-do list into the database. If the user is not
    logged in, it redirects to the home page.
    '''
    
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves the to-do list title and description from the POST form data
            to_do_list_title = request.forms.get("title")
            to_do_list_description = request.forms.get("description")

            # insert the new to-do list into the database with the user ID
            cursor.execute('INSERT INTO to_do_list (to_do_list_title, to_do_list_description, user_id) VALUES (%s, %s, %s)', (to_do_list_title, to_do_list_description, logged_in_cookie,))
            db.commit()
    
            # redirects to the to-do list page after successful transaction
            return redirect('/to_do_list')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@delete('/delete_to_do_list', method="DELETE")
def delete_to_do_list():
    '''
    Route to delete to-do list.

    Handles DELETE requests to remove a to-do list and its associated
    task from the database. If the user is logged in, it deletes the
    to-do list idenfitided by to_do_list_id from the form data. Also
    deleted all associated tasks. If hte user is not logged in, it
    redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # get the to-do list ID from the DELETE request's form data
            to_do_list_id = request.forms.get("to_do_list_id")

            # delete associated tasks from the to-do list
            cursor.execute('DELETE FROM to_do_lists_task WHERE category_id = %s;', (to_do_list_id,))
            db.commit()

            # delete the to-do list itself, ensuring it belongs to the logged-in user
            cursor.execute('DELETE FROM to_do_list WHERE id = %s  AND user_id = %s', (to_do_list_id, logged_in_cookie))
            db.commit()

            print("todolist id:", to_do_list_id)

            # render the to-do list page after successful deletion
            return template('/to_do_list')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route('/add_task_to_do_list', method='POST')
def add_task_to_do_list():
    '''
    Route to add a task to a to-do list.

    Handles the POST requests to add a task to a specified to-do list.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # get the task and title of the to-do list from the form data
            task = request.forms.get("task")
            to_do_list_title = request.forms.get("choice")

            # retrieves teh category ID of the to-do lsit using its title and logged in user ID
            cursor.execute('SELECT id FROM to_do_list WHERE to_do_list_title = %s AND user_id = %s', (to_do_list_title, logged_in_cookie))
            category_id = cursor.fetchone()[0]

            # insert the new task into the 'to_do_lists_task' table, associating it with the correct category
            cursor.execute('INSERT INTO to_do_lists_task (user_id, category_id, task) VALUES (%s, %s, %s)', (logged_in_cookie, category_id, task))
            db.commit()

            # redirects the user to the to-do list page after successfully adding the task
            return redirect('/to_do_list')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route('/update_checkbox', method='POST')
def update_checkbox():
    '''
    Route to update the checkbox state of a task.

    This function handles requests to update the 'finished' state of
    a task in a to-do list. It retrieves the task ID and the new
    checkbox state from the form data. If the user is logged in, it
    updates the task's 'finished' status in the database.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    
    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()
            
            # retrieve the task ID and the new checkbox state from the POST request's form data
            task_id = request.forms.get("task_id")
            checked = request.forms.get("checked")

            # update the "finished" status of the specified task in the database
            cursor.execute('UPDATE to_do_lists_task SET finished = %s WHERE id = %s', (checked, task_id))
            db.commit()
            
            print("task id:", task_id)

            # redirects to the to-do list page after updating the task
            return redirect('/to_do_list')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
            
@route('/calendar')
def calendar():

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            return template('calendar', user_info=get_user_info(logged_in_cookie, cursor))
        finally:
        # close database connection
            cursor.close()
            db.close()
    else:
        return redirect('/')
    
@route('/add_event', method=['GET', 'POST'])
def add_event():
    '''
        This function adds events to the events.json file
    '''
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:

        title = request.forms.get('event_name')
        description = request.forms.get('event_description')
        all_day = request.forms.get('all_day')
        start_date = request.forms.get('start_date')
        end_date = request.forms.get('end_date')

        if all_day:
            # open Json FIle
            with open('static/json/events.json', 'r') as file:
                events = json.load(file)['events']

            # This creates incroment for id:s
            for event in events:
                max_id = int(event.get('id', 0))
                id_for_new_event = max_id + 1

            add_event = {
                "id": str(id_for_new_event),
                "user_id": str(logged_in_cookie),
                "title": title,
                "description": description,
                "start": start_date,
                "end": end_date
            }

            events.append(add_event)

            # Write updated events back to the JSON file
            with open('static/json/events.json', 'w') as file:
                json.dump({"events": events}, file, indent=4)

            return redirect('/calendar')
        else:
            start_time = request.forms.get('start_time')
            end_time = request.forms.get('end_time')

            # open Json FIle
            with open('static/json/events.json', 'r') as file:
                events = json.load(file)['events']

            # This creates incroment for id:s
            for event in events:
                max_id = int(event.get('id', 0))
                id_for_new_event = max_id + 1

            add_event = {
                "id": str(id_for_new_event),
                "user_id": str(logged_in_cookie),
                "title": title,
                "description": description,
                "start": f"{start_date}T{start_time}",
                "end": f"{end_date}T{end_time}"
            }

            events.append(add_event)

            # Write updated events back to the JSON file
            with open('static/json/events.json', 'w') as file:
                json.dump({"events": events}, file, indent=4)

            return redirect('/calendar') 

    else:
        return redirect('/')
    
@route('/edit/event', method=['GET', 'POST'])
def edit_event():
    '''
        This function edits events
    '''
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:

        id = request.forms.get('edit_event_id')
        title = request.forms.get('title')
        description = request.forms.get('description')
        start_date = request.forms.get('start_date_edit')
        start_time = request.forms.get('start_time_edit')
        end_date = request.forms.get('end_date_edit')
        end_time = request.forms.get('end_time_edit')

        # open Json FIle
        with open('static/json/events.json', 'r') as file:
            events = json.load(file)['events']

        # This creates incroment for id:s
        for event in events:
            if event["id"] == id:
                event["title"] = title
                event["description"] = description
                event["start"] = f"{start_date}T{start_time}"
                event["end"] = f"{end_date}T{end_time}"

        # Write updated events back to the JSON file
        with open('static/json/events.json', 'w') as file:
            json.dump({"events": events}, file, indent=4)

        return redirect('/calendar') 

    else:
        return redirect('/')

@route('/delete/event/<id>')
def delete_event(id):
    '''
        This function deltes specifik events
    '''
    with open('static/json/events.json', 'r') as file:
        events = json.load(file)['events']
    
    # Find the index of the event to be deleted
    index_to_delete = None
    for i, event in enumerate(events):
        if event.get('id') == id:
            index_to_delete = i
            break

    # If event ID is found, delete the event
    if index_to_delete is not None:
        del events[index_to_delete]
    
    with open('static/json/events.json', 'w') as file:
        json.dump({"events": events}, file, indent=4)
    
    return redirect("/calendar")
    
@route('/get_events')
def get_events():
    """Return a JSON object with all events that matches the users ID"""
    # Read events from the JSON file
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        with open('static/json/events.json', 'r') as file:
            all_events = json.load(file)['events']

        filtered_events = []
        for event in all_events:
            if event.get('user_id') == logged_in_cookie:
                filtered_events.append(event)

        response.content_type = 'application/json'
        
        # Return the JSON-encoded event data
        return json.dumps(filtered_events)
    else:
        return redirect('/')
    
# Calendar End

# Chat bot Start

@route('/ask_anything', method=['GET', 'POST'])
def ask_anything():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            if request.method == 'POST':

                ask = request.forms.get('question')

                return template('ask_questions', response=question(ask), user_info=get_user_info(logged_in_cookie, cursor))
            
            return template('ask_questions', response=None, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

def question(qeustion):
    url = "https://chat-gpt26.p.rapidapi.com/"

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": qeustion
            }
        ]
    }

    headers = {
        "content-type": "application/json",
        "Content-Type": "application/json",
        "X-RapidAPI-Key": "d60350b2f2mshd12f8ff9e0a36afp1c99b7jsnc6d483cf34d9",
        "X-RapidAPI-Host": "chat-gpt26.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
    
@route('/progress_table')
def progress_table():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            cursor.execute("SELECT id, project, description, spb_date, status FROM progress_bar WHERE user_id = %s;", (logged_in_cookie,))
            pbs = cursor.fetchall()

            return template('progress_table', pbs=pbs, user_info=get_user_info(logged_in_cookie, cursor))

        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

@route('/add_project', method='POST')
def add_project():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:

            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            
            project = request.forms.get("task")
            description = request.forms.get("description")
            spb_date = request.forms.get("deadline_date")
            status = 'not_started'


            cursor.execute('INSERT INTO progress_bar(user_id, project, description, spb_date, status) VALUES (%s, %s, %s, %s, %s)', (logged_in_cookie, project, description, spb_date, status))
            db.commit()

            # Redirect to progress table
            return redirect('/progress_table')
        
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:

        # Redirect to login page for unathenticated users
        return redirect('/')
    
@route ('/update_status', method='POST')
def update_status():
        logged_in_cookie = request.get_cookie('loggedIn')
        if logged_in_cookie:
            try:
                # Database Connection
                db = make_db_connection()
                cursor = db.cursor()

                task_id = request.forms.get("task_id")
                new_status = request.forms.get("new_status")

                # return new_status

                cursor.execute('UPDATE progress_bar SET status = %s WHERE id = %s', (new_status, task_id))
                db.commit()
                
                # Redirect to progress table
                return redirect('/progress_table')
            finally:

                # Closing Database connection after it's been used
                cursor.close()
                db.close()

        else:
            # Redirect to login page for unathenticated users
            return redirect('/')

@route ('/delete_task', method='POST')
def delete_task():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            #Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            # Extract task ID from the request body
            task_id = request.forms.get("task_id")

            cursor.execute('DELETE FROM progress_bar WHERE id = %s AND user_id = %s', (task_id, logged_in_cookie))
            db.commit()
            
            print("task_id:", task_id)
            # Redirect to progress table after deletion
            return redirect('/progress_table')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        # Redirect to login page for unauthenticated users
        return redirect('/')
     
@route('/static/<filepath:path>')
def server_static(filepath):
    '''
        returns static files from the folder
        "static"
    '''
    print(filepath)
    return static_file(filepath, root='static')



if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)