#from crypt import methods
from bottle import route, run, template, static_file, request, redirect, response, delete
import json
import os
from db import make_db_connection

@route('/register')
def register():
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        return template('register', message=None)

@route('/register/<message>')
def register(message):
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        return template('register', message=message)

@route('/register/add/user', method=['post'])
def add_user():
    '''
    This function adds user to the database after they have submited their information on the registration page.
    '''
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()
            if request.method == 'POST':
                first_name = request.forms.get('first_name')
                last_name = request.forms.get('last_name')
                email = request.forms.get('email')
                password = request.forms.get('password')


                # Make Sure Email doesn't already exist
                cursor.execute('select * from user_info where email=%s', (email,))
                does_mail_already_exist = cursor.fetchall()
                if does_mail_already_exist:
                    return redirect('/register/Email Already Exists')

                cursor.execute('insert into user_info (name, lastname, email, password) values (%s, %s, %s, %s)', (first_name, last_name, email, password))
                db.commit()

                return redirect('/login')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()

@route('/login', method=['GET', 'POST'])
def login():
    '''
    This function shows user shows user the loginpage and it logges them in if they entered the right info
    '''
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()
            if request.method == 'POST':
                email = request.forms.get('email')
                password = request.forms.get('password')

                cursor.execute('select * from user_info where email=%s and password=%s', (email, password))
                user = cursor.fetchone()

                if user:
                    # Set a cookie indicating the user is logged in
                    response.set_cookie('loggedIn', str(user[0]))
                    return redirect('/overview')
                else:
                    return template('login', email_or_password_wrong=True)
            else:
                return template('login', email_or_password_wrong=False)
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()

@route('/')
def index():
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        return template('index')

@route('/overview')
def overview():
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            cursor.execute('SELECT * FROM to_do_list WHERE user_id = %s', (logged_in_cookie))
            todos = cursor.fetchall()

            return template('overview', todos=todos, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')
    
@route('/update/user/info', method=['GET', 'POST'])
def update_user_info():
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            first_name = request.forms.get('first_name')
            last_name = request.forms.get('last_name')
            email = request.forms.get('email')
            password = request.forms.get('password')
            image = request.files.get('pic')

            if image:
                # Get the original filename
                filename = image.filename

                # Construct the full file path and save
                filepath = os.path.join('static/pic/user_profile_pictures', filename)
                image.save(filepath)

                cursor.execute('''
                update memosync.user_info
                set profile_picture = %s
                where id = %s
                ''', (filename, logged_in_cookie))
                db.commit()

            cursor.execute('''
            update memosync.user_info
            set name = %s, lastname = %s, email = %s, password = %s
            where id = %s
            ''', (first_name, last_name, email, password, logged_in_cookie))
            db.commit()
            
            # Take User Back To The Previous Page
            return redirect(request.get_header('Referer'))
        except:
            return redirect(request.get_header('Referer'))
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

def get_user_info(id, cursor):
    '''
    This function gets the users informaiton, so that they can change or update it.
    '''
    cursor.execute('select * from user_info where id = %s', (id))
    return cursor.fetchone()

@route('/logout', method=['GET', 'POST'])
def logout():
    """Logs out a user"""
    # Make sure they are logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        # Deleting The Cookie
        response.set_cookie('loggedIn', '', expires=0)
        return redirect('/')
    else:
        return redirect('/')

@route('/to_do_list')
def to_do_list():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            cursor.execute('SELECT * from to_do_list where user_id = %s', (logged_in_cookie))
            category = cursor.fetchall()

            cursor.execute('SELECT * from to_do_lists_task where user_id = %s', (logged_in_cookie))
            tasks = cursor.fetchall()

            return template('to_do_list', category=category, tasks=tasks, user_info=get_user_info(logged_in_cookie, cursor))

        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

@route('/delete_to_do_list', method=['GET', 'POST'])
def delete_to_do_list():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            values = request.forms.getall('checkbox_todo')

            for value in values:
                cursor.execute('delete from to_do_lists_task where task = %s and user_id = %s', (value, logged_in_cookie))
            db.commit()
            
            return redirect('to_do_list')

        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

@route('/create_to_do_list', method='POST')
def create_to_do_list():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            to_do_list_title = request.forms.get("title")
            to_do_list_description = request.forms.get("description")

            cursor.execute('INSERT INTO to_do_list (to_do_list_title, to_do_list_description, user_id) VALUES (%s, %s, %s)', (to_do_list_title, to_do_list_description, logged_in_cookie,))
            db.commit()

            return redirect('/to_do_list')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

@delete('/delete_to_do_list/<to_do_list_id:int>', method="DELETE")
def delete_to_do_list(to_do_list_id):
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            cursor.execute('DELETE FROM to_do_lists_task WHERE category_id = %s;', (to_do_list_id,))
            db.commit()
            cursor.execute('DELETE FROM to_do_list WHERE id = %s', (to_do_list_id,))
            db.commit()
            return template('/to_do_list')
        
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')

@route('/add_task_to_do_list', method='POST')
def add_task_to_do_list():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            task = request.forms.get("task")
            to_do_list_title = request.forms.get("choice")

            cursor.execute('SELECT id FROM to_do_list WHERE to_do_list_title = %s AND user_id = %s', (to_do_list_title, logged_in_cookie))
            category_id = cursor.fetchone()[0]

            cursor.execute('INSERT INTO to_do_lists_task (user_id, category_id, task) VALUES (%s, %s, %s)', (logged_in_cookie, category_id, task))
            db.commit()

            return redirect('/to_do_list')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    else:
        return redirect('/')
            
@route('/calendar')
def calendar():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            return template('calendar', user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # Closing Database connection after it's been used
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
        start_date = request.forms.get('start_date')
        start_time = request.forms.get('start_time')
        end_date = request.forms.get('end_date')
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

@route('/add_event', method=['GET', 'POST'])
def add_event():
    '''
        This function adds events to the events.json file
    '''
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:

        title = request.forms.get('event_name')
        start_date = request.forms.get('start_date')
        start_time = request.forms.get('start_time')
        end_date = request.forms.get('end_date')
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
            task_id = request.json.get("task_id")

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