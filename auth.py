import os
import urllib
import requests
import json
import dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        os.chdir('.')
        config = dotenv.dotenv_values('.env')
        url = self.path
        qs = urllib.parse.parse_qs(url)
        if '/?code' in qs:
            code = qs['/?code'][0]
            params = {
                "grant_type": "authorization_code",
                "client_id": config['CLIENT_ID'],
                "client_secret": config['CLIENT_SECRET'],
                "code": code
            }
            r = requests.get(config['OAUTH_URL'], params=params)
            if r.status_code == 200:
                with open('auth_data.json', 'w') as f:
                    json.dump(r.json(), f)
                self.send_response(200)
                self.send_header('content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Success')
            else:
                self.send_response(400)
                self.send_header('content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'Error')
        else:
            user_url = config['PORTAL_URL'] + \
                'oauth/authorize/?client_id='+config['CLIENT_ID']
            self.send_response(401)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            html = '<a href="'+user_url+'">Authorize through your Bitrix24</a>'
            self.wfile.write(html.encode('utf8'))


def initAuth():
    server = HTTPServer(server_address=('0.0.0.0', 3000),
                        RequestHandlerClass=requestHandler)
    print('Server is listening on',
          server.server_address[0], server.server_address[1])
    while not os.path.isfile('auth_data.json'):
        server.handle_request()
    print('Server shutdown')


def refreshAuth():
    os.chdir('.')
    with open("auth_data.json", "r") as f:
        auth_data = json.load(f)
    config = dotenv.dotenv_values('.env')
    refresh_params = {
        "grant_type": "refresh_token",
        "client_id": config['CLIENT_ID'],
        "client_secret": config['CLIENT_SECRET'],
        "refresh_token": auth_data["refresh_token"]
    }
    rf_r = requests.get(config['OAUTH_URL'], params=refresh_params)
    if rf_r.status_code == 200:
        with open('auth_data.json', 'w') as f:
            json.dump(rf_r.json(), f)
    return rf_r.json()
