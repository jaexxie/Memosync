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

@route('/static/<filepath:path>')
def server_static(filepath):
    '''
        Returnerar statiska filer från mappen
        "static"
    '''
    print(filepath)
    return static_file(filepath, root='static')


run(host='localhost', port=8080, debug=True)