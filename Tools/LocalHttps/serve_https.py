import http.server
import os
import ssl

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Research', 'RuntimeConfig'))
os.chdir(ROOT)
server = http.server.ThreadingHTTPServer(('127.0.0.1', 5443), http.server.SimpleHTTPRequestHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    os.path.join(os.path.dirname(__file__), 'server.crt'),
    os.path.join(os.path.dirname(__file__), 'server.key'),
)
server.socket = context.wrap_socket(server.socket, server_side=True)
print('Cloud Grand Cross local HTTPS listening on 127.0.0.1:5443', flush=True)
server.serve_forever()
