from bottle import route, run, template, static_file, request, redirect, response
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

            return template('overview', user_info=get_user_info(logged_in_cookie, cursor))
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

            # Get the data from the form
            first_name = request.forms.get('first_name')
            last_name = request.forms.get('last_name')
            email = request.forms.get('email')
            password = request.forms.get('password')
            image = request.files.get('pic')  # Retrieve the file object

            if image:
                filename = image.filename  # Get the original filename
                filepath = os.path.join('static/pic/user_profile_pictures', filename)  # Construct the full file path
                
                # Save the file to the specified directory with its original filename
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

            cursor.execute("SELECT memosync.to_do_list.*, memosync.to_do_lists_task.* FROM memosync.to_do_list left JOIN memosync.to_do_lists_task ON memosync.to_do_list.id = memosync.to_do_lists_task.category_id WHERE to_do_list.user_id = %s;", (logged_in_cookie,))
            to_dos = cursor.fetchall()

            return template('to_do_list', to_dos=to_dos, user_info=get_user_info(logged_in_cookie, cursor))

        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    return template('to_do_list')

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

@route('/add_task_to_do_list', method='POST')
def create_to_do_list():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            task = request.forms.get("task")
            to_do_list_title = request.forms.get("choice")

            cursor.execute('SELECT id FROM to_do_list WHERE to_do_list_title = %s AND user_id = %s', (to_do_list_title, logged_in_cookie))
            category_id = cursor.fetchone()

            cursor.execute('INSERT INTO to_do_lists_task (user_id, category_id, task) VALUES (%s, %s, %s)', (logged_in_cookie, category_id, task))
            db.commit()

            return redirect('/to_do_list')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
            

@route('/calendar')
def calendar():
    logged_in_cookie = request.get_cookie('loggedIn')
    return template('calendar')

@route('/progress_table')
def progress_table():
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        try:
            # Database Connection
            db = make_db_connection()
            cursor = db.cursor()

            cursor.execute("SELECT project, description, spb_date, status FROM progress_bar WHERE user_id = %s;", (logged_in_cookie,))
            pbs = cursor.fetchall()

            return template('to_do_list', pbs=pbs, user_info=get_user_info(logged_in_cookie, cursor))

        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
    return template('to_do_list')

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
            status = request.forms.get("status")

            cursor.execute('INSERT INTO progress_bar(project, description, spb_date, status) VALUES (%s, %s, %s, %s)', (logged_in_cookie, project, description, spb_date, status))
            db.commit()

            return redirect('/progress_bar')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()

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