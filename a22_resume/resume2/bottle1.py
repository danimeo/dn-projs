import sys

from bottle import *

app = default_app()


def static_routing(paths_with_dot, formats):
    for path, format in zip(paths_with_dot, formats):
        app.route('{}/<filename:re:.*\.{}>'.format(path[1:], format))(lambda filename: static_file(filename, root=path))


app.route('{}/<filename>'.format('/assets/images'))(lambda filename: static_file(filename, root='./assets/images'))
app.route('{}/<filename>'.format('/assets/css'))(lambda filename: static_file(filename, root='./assets/css'))
app.route('{}/<filename>'.format('/assets/js'))(lambda filename: static_file(filename, root='./assets/js'))
app.route('{}/<filename>'.format('/assets/plugins'))(lambda filename: static_file(filename, root='./assets/plugins'))
app.route('{}/<filename>'.format('/assets/plugins/bootstrap'))(lambda filename: static_file(filename, root='./assets/plugins/bootstrap'))


@app.route('/resume')
def signup():
    return template('index')



run(host='0.0.0.0', port=8100)
