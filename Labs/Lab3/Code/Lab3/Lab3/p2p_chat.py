import threading
import socket
import datetime
import time
from enum import Enum

commands = {
        'NONE' : 0,
        'TALK' : 1,
        'JOIN' : 2,
        'LEAVE': 3,
        'WHO'  : 4,
        'QUIT' : 5
    }

def init(ip_address='127.0.0.1', port = 8080):
    user_name = input('Enter your name: ')
    threading.Thread(target=sender, args=(user_name, ip_address, port)).start()
    threading.Thread(target=receiver, args=(port,)).start()
    
def sender(user_name, ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    application_message = build_message('/JOIN', user_name)
    broadcast(s, port, application_message)
    while True:
        user_message = ''
        try:
            user_message = input()
        except EOFError:
            return
        application_message = build_message(user_message, user_name)
        command = parse_command(application_message)[1]
        broadcast(s, port, application_message)
    
def receiver(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('',port))
    users = []
    while True:
        application_message = s.recv(4096)
        
        (user_name,user_command,user_message) = parse_message(application_message)
        
        timestamp = st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        
        msg = ''
        
        user_command = int(user_command)
        
        if user_command != commands['NONE']:
            if user_command == commands['TALK']:
                msg = f'[{user_name}]: {user_message}'
                
            elif user_command == commands['JOIN']:
                msg = f'{user_name} joined!'
                users.append(user_name)
                
            elif user_command == commands['LEAVE']:
                msg = f'{user_name} left!'
            
            elif user_command == commands['WHO']:
                msg = str(users)
                
            print(f'{timestamp} {msg}')
        
def broadcast(socket, port, message):
    socket.sendto(message.encode(), ('255.255.255.255', port))
        
def build_message(user_message, user_name):
    cmd, msg = parse_command(user_message)
    return f'user:{user_name}\ncommand:{cmd}\nmessage:{msg}\n\n'

def parse_message(application_message):
    application_message = application_message.decode()
    lines = application_message.split('\n')
    user = lines[0].split(':')
    command = lines[1].split(':')
    message = lines[2].split(':')
    return user[1], command[1], message[1]

def parse_command(user_message):
    if user_message[0] == '/':
        d = user_message.find(' ')
        command = ''
        message = ''
        if d > 0:
            command = user_message[1:d]
            message = user_message[d+1:]
        else:
            command = user_message[1:]
            
        command = command.upper()
        
        if command not in commands.keys():
            command = commands['NONE']
        else:
            command = commands[command]
        return command, message
    else:
        return commands['TALK'], user_message
init()