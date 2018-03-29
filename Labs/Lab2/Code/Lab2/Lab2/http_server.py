import socket
import threading
import os


#Default values
LOCALHOST = ''
HTTP_PORT = 80;
BUFFER = 4096
ROOT_DIRECTORY = 'public'

#Possible responses codes to handle requests
RESPONSE_CODES = {
        '200': 'OK',
        '404': 'Not Found'
    }

#Run a single instance of a server
def run_server(host = LOCALHOST, port = HTTP_PORT, verbose = False, directory = ROOT_DIRECTORY):
    init(directory)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        listener.bind((host, port))
        listener.listen()
        print('HTTP server is listening at ', port)
        while True:
            conn, addr = listener.accept()
            threading.Thread(target=handle_client, args=(conn, addr, verbose, directory)).start()
    finally:
        listener.close()

#Create directory for file server
def init(directory):
    # create server directory if it doesnt exists
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#Handle data sent by connected clients
def handle_client(conn, addr, verbose, directory):
    if verbose:
        print(f'New client from {addr}')
    try:
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break
            
            pos = data.find(b"Content-Length: ")
            if pos >= 0:
                d = data[pos + len("Content-Length: "):]
                cl = int(d[:d.find(b"\r")])
                if len(data[data.find(b"\r\n\r\n") + len("\r\n\r\n"):]) < cl:
                    data += conn.recv(cl)
            response = process_data(conn, data, directory)
            if verbose:
                print(f'Response sent to {addr} : {response}')
            
    finally:
        if verbose:
            print(f'Connection closed from {addr}')
        conn.close()

lock = threading.Lock()

#Process the data received by a client
def process_data(conn, data, directory):
    seperator = data.find(b' ')
    
    req_type = data[:seperator].decode('utf-8')
    
    data = data[seperator + 1:]
    
    seperator = data.find(b' ')
    
    path = data[:seperator].decode('utf-8')
    
    full_path = directory + path
    
    if path != '/' :
        path = path + '/'
    
    data = data[seperator + 1:]
    
    seperator = data.find(b'\r\n\r\n')
    
    # Used in post request
    body = data[seperator+4:].decode('utf-8')
    
    code = '200'
    
    if req_type == 'GET':
        html_body = ''
        ctype = 'text/html'
        if os.path.isdir(full_path):
            html_body = '<html><body>';
            html_body += f'</br><h1>Contents of Directory: {path}</h1></br>'
            files = os.listdir(full_path)
            html_body += '<ul>'
            for file in files:
                html_body += f'<li><a href=\"{path}{file}\">{file}</a></li>'
            html_body += '</ul>'
            html_body += '</body></html>'
        elif os.path.isfile(full_path):
            #html_body += f'</br><h1>Contents of File: {path}</h1></br>'
            ctype = 'text/plain'
            with lock:
                html_body += open(full_path, 'r').read()
        else:
            code = '404'
            html_body += f'<h1>{code} {RESPONSE_CODES[code]}</h1>'
        
        response = generate_response(code, html_body, ctype).encode()
        conn.sendall(response)
        return html_body
        
    elif req_type == 'POST':
        #Lock the file
        with lock:
            output = open(full_path,"w")
            print('writing: ' + body)
            output.write(body)
            output.close()
        response = generate_response(code, '').encode()
        conn.sendall(response)
        return ''
    return ''
        
    
def generate_response(code, body, ctype='text\html'):
    return f'HTTP/1.0 {code} {RESPONSE_CODES[code]}\r\n' + \
        f'Content-Length: {len(body)}\r\n' + \
        f'Content-Type: {ctype}\r\n' + \
        f'Content-Disposition: inline\r\n' +\
        f'Connection: Closed\r\n\r\n' + body
        
    