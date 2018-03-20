import argparse
import socket
import threading
import os
import json

def run_server(host, port, v, d):
	if not os.path.exists(d):
		os.makedirs(d)
	listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		listener.bind((host, port))
		listener.listen()
		print('server is listening at ', p)
		while True:
			conn, addr = listener.accept()
			threading.Thread(target=handle_client, args=(conn, addr, v, d)).start()
	finally:
		listener.close()

mutex = threading.Lock()		
buf = 2048		
def handle_client(conn, addr, v, d):
	if v:
		print(f'Incomming client from ' + str(addr))
	try:
		while True:
			data = conn.recv(buf)
			if not data:
				break
				
			delimiter = data.find(b'\r\n\r\n')
			header = data[:delimiter].decode('utf-8')
			body = data[delimiter+4:].decode('utf-8')
			
			lines = header.splitlines()
			line1 = lines[0]
			method = line1[:line1.find(' ')]
			path = (line1[line1.find(' ') + 1 : line1.find(' ') + 1 + line1[line1.find(' ') + 1:].find(' ')])
			relative_path = d + path
			path = path + '/' if path != '/' else path
			response_body = {}
			code = '200'
			if method == 'POST':
				with mutex:
					output = open(relative_path,"w")
					output.write(body)
					output.close()
			elif method == 'GET':
				if os.path.isfile(relative_path):
					with mutex:
						response_body['file'] = {'path': relative_path, 'contents': open(relative_path, 'r').read()}
				elif os.path.isdir(relative_path):
					files = os.listdir(relative_path)
					response_body['files'] = files
				else:
					code = '404'
			
			
			msg = ''
			if code == '200':
				msg = 'OK'
			elif code == '404':
				msg = 'Not Found'
			
			response_body['status'] = {'code': code, 'message': msg}
			response_body = json.dumps(response_body, indent=4)
			
			response =  'HTTP/1.0 ' + code + ' ' + msg + '\r\n' + \
			'Content-Length: ' + str(len(response_body)) + '\r\n' + \
			'Content-Type: application/json\r\n' + \
			'Content-Disposition: inline\r\n\r\n' + response_body

			response = response.encode()
			conn.sendall(response)
				
	finally:
		if v:
			print('Client closed connection from ' + str(addr))
		conn.close()
		
parser = argparse.ArgumentParser()
parser.add_argument("-d")
parser.add_argument("-p")
parser.add_argument("-v", action='store_true')
args = parser.parse_args()
v = args.v
p = args.p if args.p else 80
d = args.d if args.d else 'root'
run_server('', int(p), v, d)	
