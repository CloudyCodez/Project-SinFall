import http.server
import os
import ssl
import threading
import urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Research', 'RuntimeConfig'))


class LocalContentHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean = urllib.parse.urlsplit(path).path.lstrip('/')
        if clean.startswith('nmss/'):
            clean = os.path.basename(clean)
        return os.path.join(ROOT, *clean.split('/'))

    def do_GET(self):
        clean_path = urllib.parse.urlsplit(self.path).path
        local_path = self.translate_path(self.path)
        allowed = (
            clean_path.startswith('/nanagb/config/')
            or clean_path in ('/nanagb/connection.txt', '/nanagb/utc_standard.html')
        )
        if clean_path.startswith('/nmss/'):
            local_path = self.translate_path(self.path)
            allowed = True
        if allowed and not os.path.isfile(local_path):
            self.send_error(404, 'Missing local bootstrap fixture')
            print(f'Missing local bootstrap fixture: {clean_path}', flush=True)
            return
        super().do_GET()


def serve_http():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 5100), LocalContentHandler)
    print('Cloud Grand Cross local HTTP listening on 127.0.0.1:5100', flush=True)
    server.serve_forever()


def serve_https():
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 5443), LocalContentHandler)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        os.path.join(os.path.dirname(__file__), 'server.crt'),
        os.path.join(os.path.dirname(__file__), 'server.key'),
    )
    server.socket = context.wrap_socket(server.socket, server_side=True)
    print('Cloud Grand Cross local HTTPS listening on 127.0.0.1:5443', flush=True)
    server.serve_forever()


threading.Thread(target=serve_http, daemon=True).start()
serve_https()
