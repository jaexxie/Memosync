from bottle import route, run, template, static_file, request, redirect, response
from db import make_db_connection

@route('/register')
def register():
    return template('register')

@route('/register/add/user', method=['post'])
def add_user():
    '''
    This function adds user to the database after they have submited their information on the registration page.
    '''
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
                response.set_cookie('loggedIn', user[0], secret=int(user[0]))
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
    return template('index')

@route('/overview')
def overview():
    return template('overview')

@route('/to_do_list')
def to_do_list():
    return template('to_do_list')

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