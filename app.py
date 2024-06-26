#from crypt import methods
from datetime import date
import datetime
from random import random
from unicodedata import category
from bottle import route, run, template, static_file, request, redirect, response, delete
import json
import os
from pymysql import Date
from db import make_db_connection, does_the_token_match_the_users_token
import requests
from passlib.hash import pbkdf2_sha256

# HOME PAGE

@route('/')
def index():
    '''
    Route for index page.

    Checks if the user is logged in and redirected to the overview
    page, otherwise the user is redicted to the index template.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')

    if logged_in_cookie:
        # user is logged in and redicted to the overview page
        return redirect('/overview')
    else:
        # user is not logged in and remains on the index page
        return template('index')

# REGISTER

@route('/register')
def register():
    '''
    Route for registration page.

    If the user is logged in, it redirects to the overview page, if
    the user is not logged in, the user remains on the registation page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    
    if logged_in_cookie:
        return redirect('/overview')
        # user is logged in and redicted to the overview page
    else:
        # user is not logged in and remains on the register page
        return template('register', message=None)

@route('/register/<message>')
def send_message_to_users_registering(message):
    '''
    Route for regristration page with a message parameter.

    If the user is logged in, it redirects to the overview page, if
    the user is not logged in, the user remains on the registation
    with the given message.
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

    If the user is already logged in, it verifies the session token
    and redirects to the overview page. if the user is not logged in
    it processes the registration.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
   
    token = request.get_cookie('token')

    if logged_in_cookie:
        # verifies the token to ensure it matches the user's token
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            # if tokens do not match, clear cookies and redirect to the home page
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            return redirect('/')
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
                first_name = getattr(request.forms, 'first_name')
                last_name = getattr(request.forms, 'last_name')
                email = request.forms.get('email')
                password = request.forms.get('password')

                # ensures the first name only contains alphabetic characters
                if first_name.isalpha():
                    # ensures the last name contains only alphabetic characters
                    if last_name.isalpha():
                        # check the length of the first name
                        if len(first_name) <= 50:
                            # check the length of the last name
                            if len(last_name) <= 50:
                                # ensures the email does not already exist in the database
                                cursor.execute('SELECT * FROM user_info WHERE email=%s', (email,))
                                does_mail_already_exist = cursor.fetchall()
                                
                                if does_mail_already_exist:
                                    # if email already exists, redirect with the message
                                    return redirect('/register/Email already exists')
                                
                                # hashes the password and creates a token
                                hash_password = pbkdf2_sha256.hash(password)
                                token = f"{hash_password}RAYANN{datetime}"
                            
                                # inserts the new user into the ddatabase
                                cursor.execute('INSERT INTO user_info (name, lastname, email, password, token) VALUES (%s, %s, %s, %s, %s)', (first_name, last_name, email, hash_password, token))
                                # commits the transaction
                                db.commit()

                                # redirects the user to the login page after successful registration
                                return redirect('/login')
                            else:
                                return redirect('/register/Lastname Can Not Be Longer Than 50 Characters')
                        else:
                            return redirect('/register/Firstname Can Not Be Longer Than 50 Characters')
                    else:
                        return redirect('/register/Lastname Can Not Include Any Non Alphabetic Characters')
                else:
                    return redirect('/register/Firstname Can Not Include Any Non Alphabetic Characters')
        finally:
            # close database connection
            cursor.close()
            db.close()

# LOGIN

@route('/login', method=['GET', 'POST'])
def login():
    '''
    Route for the login page.

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

                # checks if the user exists with the given email
                cursor.execute('SELECT * FROM user_info WHERE email=%s', (email))
                user = cursor.fetchone()

                if user is None:
                    # no user found with the given email
                    return template('login', email_or_password_wrong=True, email_not_found=True)
                else:
                    # retrieves the stored hash password
                    hash = str(user[4])

                    if pbkdf2_sha256.verify(password, hash):
                        # if the user exists, sets a cookie indicating they are logged in
                        response.set_cookie('loggedIn', str(user[0]))
                        response.set_cookie('token', str(user[6]))

                        # redirects the user to the overview page after successful login
                        return redirect('/overview')
                    else:
                        # incorrect password
                        return template('login', email_or_password_wrong=True)
            else:
                # renders the login page without error
                return template('login', email_or_password_wrong=False)
        finally:
            # close database connection
            cursor.close()
            db.close()

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
        response.set_cookie('token', '', expires=0)
        # redirects to the home page after logging out
        return redirect('/')
    else:
        # if not logged in, redirects to the home page
        return redirect('/')

# OVERVIEW PAGE

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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves the user information from the form
            first_name = getattr(request.forms, 'first_name')
            last_name = getattr(request.forms, 'last_name')
            email = request.forms.get('email')
            image = request.files.get('pic')

            if image.filename != 'empty':
                
                # save the image to the specified directory
                filename = image.filename

                # update the user's profile picture in the database
                cursor.execute("UPDATE memosync.user_info SET profile_picture = %s WHERE id = %s", (filename, logged_in_cookie))
                db.commit()

                filepath = os.path.join('static/pic/user_profile_pictures', filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
                image.save(filepath)

            # update the user's information in the database
            cursor.execute("UPDATE memosync.user_info SET name = %s, lastname = %s, email = %s WHERE id = %s", (first_name, last_name, email, logged_in_cookie))
            db.commit()
            
            # redirects the user back to the referring page after a successful update
            return redirect(request.get_header('Referer'))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route('/delete/profile/picture', method=['GET', 'POST'])
def delete_profile_picture():
    '''
    Route to delete the user's profile picture.

    Checks if the user is logged in, verifies the session token and
    updates the user's profile picture to the database. If the user is
    not logged in, it redirects to the home page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # connect to the database
            db = make_db_connection()
            cursor = db.cursor()

            # updates the user's profile picture to a default image
            cursor.execute('UPDATE user_info SET profile_picture = %s WHERE id = %s', ('default.jpeg', logged_in_cookie))
            db.commit()

            # redirects tot he referring page after successful update
            return redirect(request.get_header('Referer'))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route('/delete/my/account', method=['GET', 'POST'])
def delete_my_account():
    '''
    Route to delete the user's account.

    Checks if the user is logged in, verifies the session token and
    deletes the user's account from the database. If the user is not
    logged in, it redirects to the home page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # verifies the token to ensure it matches the user's token
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            # if tokens do not match, clear cookies and redirect to the home page
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # connect to the database
            db = make_db_connection()
            cursor = db.cursor()

            # delete the user's account from the database
            cursor.execute('DELETE FROM user_info WHERE id = %s', (logged_in_cookie))
            db.commit()

            # redirect to the referring page agest succesful deletion
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

# TO DO LIST PAGE

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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves the to-do list title and description from the POST form data
            to_do_list_title = getattr(request.forms, "title")
            to_do_list_description = getattr(request.forms, "description")

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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # get the task and title of the to-do list from the form data
            task = getattr(request.forms, "task")
            to_do_list_title = getattr(request.forms, "choice")

            # retrieves the category ID of the to-do lsit using its title and logged in user ID
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

@route ('/delete_to_do_task', method='DELETE')
def delete_to_do_task():
    '''
    Route for deleting tasks from todo lists .

    If the user is logged in, retrived the task ID from the request
    and deletes the task from the database. If the user is not logged
    in, it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            #database connection
            db = make_db_connection()
            cursor = db.cursor()

            # extracts task ID from the request body
            task_id = request.forms.get("task_id")

            # delete associated tasks from the to-do list
            cursor.execute('DELETE FROM to_do_lists_task WHERE id = %s', ( task_id))
            db.commit()
            
            # redirect to to_do_list table after deleting the task
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
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()
            
            # retrieves the task ID and the new checkbox state from the POST request's form data
            task_id = request.forms.get("task_id")
            checked = request.forms.get("checked")

            # updates the "finished" status of the specified task in the database
            cursor.execute('UPDATE to_do_lists_task SET finished = %s WHERE id = %s', (checked, task_id))
            db.commit()
            

            # redirects to the to-do list page after updating the task
            return redirect('/to_do_list')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

# CALENDAR PAGE
          
@route('/calendar')
def calendar():
    '''
    Route for the calendar page.

    If the user is logged in, it renders teh calendar page with the
    user's information. If not logged in the user is redirected to the
    home page.
    '''
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves the current date
            current_date = datetime.date.today()
            formatted_date = current_date.isoformat()

            # renders the 'calendar' template, providing the logged-in user's information
            return template('calendar', date=formatted_date, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
        # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route('/add_event', method=['GET', 'POST'])
def add_event():
    '''
    Route for adding events to events.json file.

    If not logged in the user is redirected to the
    home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        
        # retrives event information from the form data
        title = getattr(request.forms, 'event_name')
        description = getattr(request.forms, 'event_description')
        all_day = request.forms.get('all_day')
        start_date = request.forms.get('start_date')
        end_date = request.forms.get('end_date')

        # creates a new all-day event
        if all_day:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59")

            # open the JSON file to read existing events
            with open('static/json/events.json', 'r') as file:
                events = json.load(file)['events']

            # Find the maximum event ID
            max_id = max(int(event.get('id', 0)) for event in events)
            id_for_new_event = max_id + 1

            # add form data to variable add_event
            add_event = {
                "id": str(id_for_new_event),
                "user_id": str(logged_in_cookie),
                "title": title,
                "description": description,
                "start": start_date,
                "end": end_date
            }

            # append the new event to the list of events
            events.append(add_event)

            # write updated events back to the JSON file
            with open('static/json/events.json', 'w') as file:
                json.dump({"events": events}, file, indent=4)

            return redirect('/calendar')
        else:
            # retrieves time from form data if the event is not all-day
            start_time = request.forms.get('start_time')
            end_time = request.forms.get('end_time')

            # open the JSON file to read existing events
            with open('static/json/events.json', 'r') as file:
                events = json.load(file)['events']

            # determine the new event ID by increamenting the maximum existing ID
            for event in events:
                max_id = int(event.get('id', 0))
                id_for_new_event = max_id + 1

            # add form data to variable add_event
            add_event = {
                "id": str(id_for_new_event),
                "user_id": str(logged_in_cookie),
                "title": title,
                "description": description,
                "start": f"{start_date}T{start_time}",
                "end": f"{end_date}T{end_time}"
            }

            # write updated events back to the JSON file
            events.append(add_event)

            # write updated events back to the JSON file
            with open('static/json/events.json', 'w') as file:
                json.dump({"events": events}, file, indent=4)

            return redirect('/calendar') 
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route('/edit/event', method=['GET', 'POST'])
def edit_event():
    '''
    Route for editing events in the events.json file.

    Retrieves the event ID and updated information from the form data.
    Opens the event.json file, finds the event by ID and updates the
    the relevant event. If the user is not logged, the user is
    redirected to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        
        # retrives event information from the form data
        id = request.forms.get('edit_event_id')
        title = getattr(request.forms, 'title')
        description = getattr(request.forms, 'description')
        start_date = request.forms.get('start_date_edit')
        start_time = request.forms.get('start_time_edit')
        end_date = request.forms.get('end_date_edit')
        end_time = request.forms.get('end_time_edit')
        all_day = request.forms.get('edit_all_day') == 'True'

        # open the JSON file to read existing events
        with open('static/json/events.json', 'r') as file:
            events = json.load(file)['events']

        # finds the event by ID and update the relevant details
        for event in events:
            if event["id"] == id:
                # updates event details
                event["title"] = title
                event["description"] = description

                # handles all day events
                if all_day:
                    event["start"] = start_date + 'T00:00:00'
                    event["end"] = end_date + 'T23:59:59'
                else:
                    event["start"] = f"{start_date}T{start_time}"
                    event["end"] = f"{end_date}T{end_time}"
                
        # writes the updated events back to the JSON file
        with open('static/json/events.json', 'w') as file:
            json.dump({"events": events}, file, indent=4)

        return redirect('/calendar') 
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route('/delete/event/<id>')
def delete_event(id):
    '''
        Route for deleting events from the events.json file.

        Deletes an event by finding the index of the event to be
        deleted by using the provided ID. If the event ID is found,
        the event is removed from the lsit of events and the updated
        list of events is written back to the events.json file. The
        user is then redirected to the calendar page.
    '''

    # open the JSON file to read existing events
    with open('static/json/events.json', 'r') as file:
        events = json.load(file)['events']
    
    # find the index of the event to be deleted
    index_to_delete = None
    for i, event in enumerate(events):
        if event.get('id') == id:
            index_to_delete = i
            break

    # if event ID is found, delete the event
    if index_to_delete is not None:
        del events[index_to_delete]
    
    with open('static/json/events.json', 'w') as file:
        json.dump({"events": events}, file, indent=4)
    
    return redirect("/calendar")
    
@route('/get_events')
def get_events():
    '''
    Route to retrieve all events for the logged-in user in JSON format.

    Returns all the events matching the logged-in user's ID. If the
    user is not logged in, it redirects the user to the home page-
    '''
    
    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        
        # open the JSON file to read existing events
        with open('static/json/events.json', 'r') as file:
            all_events = json.load(file)['events']

        # filters events to include only those matching the user's ID
        filtered_events = []
        for event in all_events:
            if event.get('user_id') == logged_in_cookie:
                filtered_events.append(event)

        # set the content type to JSON
        response.content_type = 'application/json'
        
        # returns the JSON filtered events
        return json.dumps(filtered_events)
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

# PROGRESS TABLE PAGE

@route('/progress_table')
def progress_table():
    '''
    Route for the progress page.

    Displays a progress table for the logged-in user by fetching data
    from the progress_bar table in the database. If the user is not
    logged in, it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieve progress bar data fro the logged-in user
            cursor.execute("SELECT id, project, description, spb_date, status FROM progress_bar WHERE user_id = %s;", (logged_in_cookie,))
            pbs = cursor.fetchall()

            # render the progresss table page with the fetched data
            return template('progress_table', pbs=pbs, user_info=get_user_info(logged_in_cookie, cursor))
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route('/add_project', method='POST')
def add_project():
    '''
    Route for adding a new project to the progress bar.

    If the user is logged in, project information is retrieved from
    the form data and inserted into the database. If the user is not
    logged in, it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves project information from the form data
            project = getattr(request.forms, "task")
            description = getattr(request.forms, "description")
            spb_date = request.forms.get("deadline_date")
            status = 'not_started'

            # inserts the new project into progress_table in the database
            cursor.execute('INSERT INTO progress_bar(user_id, project, description, spb_date, status) VALUES (%s, %s, %s, %s, %s)', (logged_in_cookie, project, description, spb_date, status))
            db.commit()

            # redirects to progress table
            return redirect('/progress_table')
        
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
    
@route ('/update_status', method='POST')
def update_status():
    '''
    Route for updating status of a task in the progress table.

    If the user is logged in, it retrieves the task ID and the new
    status from the form data and updates the database. If the user
    is not logged in, it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database Connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves teh task ID and new status from the form data
            task_id = request.forms.get("task_id")
            new_status = request.forms.get("new_status")

            # updates the status of the specified task in the progress bar
            cursor.execute('UPDATE progress_bar SET status = %s WHERE id = %s', (new_status, task_id))
            db.commit()
            
            # redirect to progress table
            return redirect('/progress_table')
        finally:
            # close database connection
            cursor.close()
            db.close()

    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route ('/delete_task', method='POST')
def delete_task():
    '''
    Route for deleting tasks from the progress table.

    If the user is logged in, retrived the task ID from the request
    and deletes the task from the database. If the user is not logged
    in, it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            #database connection
            db = make_db_connection()
            cursor = db.cursor()

            # extracts task ID from the request body
            task_id = request.forms.get("task_id")

            # deletes task from the progress_bar table
            cursor.execute('DELETE FROM progress_bar WHERE id = %s AND user_id = %s', (task_id, logged_in_cookie))
            db.commit()

            return redirect('/progress_table')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')

@route ('/update_task', method='POST')
def update_task():
    '''
    Route for editing content of a task in the progress table.

    If the user is logged in, it retrieves the task ID and the new
    content and updates the database. If the user is not logged in,
    it redirects to the home page.
    '''

    # checks if the user is already logged in by checking the 'loggedIn' cookie
    logged_in_cookie = request.get_cookie('loggedIn')
    token = request.get_cookie('token')

    if logged_in_cookie:
        # if logged in, clear the 'loggedIn' cookie to log the user out
        if not does_the_token_match_the_users_token(token, logged_in_cookie):
            response.set_cookie('loggedIn', '', expires=0)
            response.set_cookie('token', '', expires=0)
            # redirects to the home page after logging out
            return redirect('/')
        try:
            # database Connection
            db = make_db_connection()
            cursor = db.cursor()

            # retrieves task ID and new content and cell type from the form data
            task_id = request.forms.get("task_id")
            new_content = request.forms.get("new_content")
            cell_type = request.forms.get("cell_type")

            # updates the appropriate column in the progress_bar based on the cell type
            if cell_type == "task":
                # updates the project field with the new content for the given task ID
                cursor.execute('UPDATE progress_bar SET project = %s WHERE id = %s', (new_content, task_id))
            elif cell_type == "description":
                # updates the description field with the content for the given task ID
                cursor.execute('UPDATE progress_bar SET description = %s WHERE id = %s', (new_content, task_id))
            elif cell_type == "date":
                # updates the spb_date field with the new content for the given task ID
                cursor.execute('UPDATE progress_bar SET spb_date = %s WHERE id = %s', (new_content, task_id))

            #commit changes to the database
            db.commit()

            # redirect to progress table
            return redirect('/progress_table')
        finally:
            # close database connection
            cursor.close()
            db.close()
    else:
        # if the user is not logged in, redirect to the home page
        return redirect('/')
     
@route('/static/<filepath:path>')
def server_static(filepath):
    '''
        Route for returning static files.
    '''
    print(filepath)
    return static_file(filepath, root='static')

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True)