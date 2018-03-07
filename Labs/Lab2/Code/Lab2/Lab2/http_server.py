import socket
import threading
import os

HTTP_PORT = 80;
BUFFER = 4096
ROOT_DIRECTORY = 'public'

RESPONSE_CODES = {
        '200': 'OK',
        '404': 'Not Found'
    }

def run_server(host):
    init()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, HTTP_PORT))
        listener.listen()
        print('HTTP server is listening at ', HTTP_PORT)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    finally:
        listener.close()

def init():
    # create server directory if it doesnt exists
    try:
        if not os.path.exists(ROOT_DIRECTORY):
            os.makedirs(ROOT_DIRECTORY)
    except OSError:
        print ('Error: Creating directory. ' +  ROOT_DIRECTORY)


def handle_client(conn, addr):
    print(f'New client from {addr}')
    try:
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break
            
            process_data(conn, data)
            
    finally:
        print(f'Connection closed from {addr}')
        conn.close()

def process_data(conn, data):
    seperator = data.find(b' ')
    
    req_type = data[:seperator].decode('utf-8')
    
    data = data[seperator + 1:]
    
    seperator = data.find(b' ')
    
    path = data[:seperator].decode('utf-8')
    
    full_path = ROOT_DIRECTORY + path
    
    if path != '/' :
        path = path + '/'
        
    
        
    
    
    
    data = data[seperator + 1:]
    
    seperator = data.find(b'\r\n\r\n')
    
    # Used in post request
    body = data[seperator+4:].decode('utf-8')
    
    code = '200'
    
    if req_type == 'GET':
        html_body = '<html><html_body>';
        if os.path.isdir(full_path):
            html_body += f'</br><h1>Contents of Directory: {path}</h1></br>'
            files = os.listdir(full_path)
            html_body += '<ul>'
            for file in files:
                html_body += f'<li><a href=\"{path}{file}\">{file}</a></li>'
            html_body += '</ul>'
        elif os.path.isfile(full_path):
            html_body += f'</br><h1>Contents of File: {path}</h1></br>'
            html_body += open(full_path, 'r').read()
        else:
            code = '404'
            html_body += f'<h1>{code} {RESPONSE_CODES[code]}</h1>'
        html_body += '</html_body></html>'
        response = generate_response(code, html_body).encode()
        conn.sendall(response)
    elif req_type == 'POST':
        if os.path.isfile(full_path):
            os.remove(full_path)
        output = open(full_path,"w")
        output.write(body)
        output.close()
        response = generate_response(code, '').encode()
        conn.sendall(response)
    
def generate_response(code, body):
    print(body)
    return f'HTTP/1.0 {code} {RESPONSE_CODES[code]}\r\n' + \
        f'Content-Length: {len(body)}\r\n' + \
        f'Content-Type: text\html\r\n' + \
        f'Connection: Closed\r\n\r\n' + body
        
    

run_server('')