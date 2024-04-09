from bottle import route, run, template, static_file, request, redirect, response
from db import make_db_connection

@route('/register')
def register():
    # Make sure they aren't already logged in
    logged_in_cookie = request.get_cookie('loggedIn')
    if logged_in_cookie:
        return redirect('/overview')
    else:
        return template('register')

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

            cursor.execute('select * from user_info where id = %s', (logged_in_cookie))
            user_info = cursor.fetchone()

            return template('overview')
        finally:
            # Closing Database connection after it's been used
            cursor.close()
            db.close()
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

            cursor.execute("SELECT to_do_list_title, to_do_list_description FROM to_do_list WHERE user_id = %s", (logged_in_cookie,))
            to_dos = cursor.fetchall()

            return template('to_do_list', to_dos=to_dos)

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
            

@route('/calendar')
def calendar():
    return template('calendar')

@route('/progress_table')

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