import threading
import socket
import datetime
import time


def init(ip_address='127.0.0.1', port = 8080):
    user_name = input('Enter your name: ')
    print(f'Welcome {user_name}!')
    threading.Thread(target=sender, args=(user_name, ip_address, port)).start()
    threading.Thread(target=receiver, args=(port,)).start()
    
def sender(user_name, ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    while True:
        user_message = input()
        application_message = build_message(user_message, user_name)
        s.sendto(application_message.encode(), ('255.255.255.255', port))
    
def receiver(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('',port))
    while True:
        application_message = s.recv(4096)
        (user_name,user_message) = parse_message(application_message)
        timestamp = st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f'{timestamp} [{user_name}]: {user_message}')
        
def build_message(user_message, user_name):
    return f'user:{user_name}\nmessage:{user_message}\n\n'

def parse_message(application_message):
    application_message = application_message.decode()
    lines = application_message.split('\n')
    user = lines[0].split(':')
    message = lines[1].split(':')
    return user[1], message[1]

init()