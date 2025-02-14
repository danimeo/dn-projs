from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer

from datetime import datetime, timedelta

# from dcam3_dist import Distributor


class WebPageHandler(BaseHTTPRequestHandler):

    def ac_header(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE, HEAD")
        self.send_header("Access-Control-Max-Age", "3600")
        self.send_header("Access-Control-Allow-Headers", "access-control-allow-origin, authority, content-type, version-info, X-Requested-With")


    def do_GET(self):
        
        if self.path == '/':
            self.send_response(200)

            self.ac_header()

            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            t1 = 'root'
            self.wfile.write(t1.encode('utf-8'))
        elif self.path == '/now':
            self.send_response(200)

            self.ac_header()

            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            t1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print(t1.encode('utf-8'))
            self.wfile.write(t1.encode('utf-8'))
        elif self.path == '/about':
            self.send_response(200)
            self.ac_header()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>About Us</h1><p>We are a company specializing in web development.</p>')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Page Not Found</h1><p>The requested page does not exist.</p>')

filenames = {
    'balance': 'dcam_data/finance/balance.txt',
    'distribution': 'dcam_data/distributions/time_collection.txt',
    'prices': 'dcam_data/finance/prices.txt',
    'users_db': 'users.db',
    'time_db': 'time.db',
}
remote = ('localhost', 8215)

# distr = Distributor(filenames, remote)
# distr.read_from_file()
server = TCPServer(remote, WebPageHandler)
server.serve_forever()
