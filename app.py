from bottle import route, run, template, static_file

@route('/')
def index():
    return template('index')

@route('/register')
def register():
    return template('register')

@route('/login')
def login():
    return template('login')

@route('/header')
def register():
    return template('header_base')

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


run(host='localhost', port=8080, debug=True)