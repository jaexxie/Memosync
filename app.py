from bottle import route, run, template, static_file

@route('/')
def index():
    return template('index')

@route('/register')
def register():
    return template('register')

@route('/static/<filename>')
def server_static(filename):
    '''
        Returnerar statiska filer från mappen
        "static"
    '''
    return static_file(filename, root='static')


run(host='localhost', port=8080, debug=True)