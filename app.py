from bottle import route, run, template, static_file

@route('/')
def hello():
    return template('index')

@route('/static/<filename>')
def server_static(filename):
    '''
        Returnerar statiska filer från mappen
        "static"
    '''
    return static_file(filename, root='static')


run(host='localhost', port=8080, debug=True)