import sys
import threading
import socket
import datetime
import time

commands = {
        'NONE' : 0,
        'TALK' : 1,
        'JOIN' : 2,
        'LEAVE': 3,
        'WHO'  : 4,
        'QUIT' : 5,
        'PING' : 6,
        'PRIVATE-TALK' : 7
    }

terminate = False
users = {}
sem = threading.Semaphore(value=0)

def init(ip_address='', port = 8080):
    user_name = input('Enter your name: ')
    threading.Thread(target=sender,     args=(user_name, ip_address, port)).start()
    threading.Thread(target=receiver,   args=(user_name, ip_address, port)).start()
    
    
def sender(user_name, ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    global sem
    sem.acquire()
    application_message = build_message('/JOIN', user_name)
    broadcast(s, port, application_message)
    global terminate
    while True:
        if terminate == True:
            quit()
            
        user_message = ''
        try:
            user_message = input()
        except EOFError:
            return
        
        application_message = build_message(user_message, user_name)
        
        # Command and message seperated
        user_command, msg = parse_command(user_message)
        

        if user_command == commands['LEAVE']:
            broadcast(s, port, application_message)
            unicast(s, port, build_message('/QUIT', user_name), ip_address)
            
        elif user_command == commands['WHO']:
            unicast(s, port, application_message, ip_address)
            
        elif user_command == commands['PRIVATE-TALK']:
            words = msg.split(' ')
            user = words[0];
            msg = ' '.join(words[1:])
            unicast(s, port, build_message(f'/PRIVATE-TALK {msg}', user_name), users[user])
        
        else:
            broadcast(s, port, application_message)


def receiver(user_name, ip_address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip_address,port))
    global terminate
    global users
    global sem
    sem.release()
    while True:
        if terminate == True:
            quit()
        
        application_message, addr = s.recvfrom(4096)
        #print(f'RECEIVED FROM: {addr}')
        (recv_user_name,user_command,user_message) = parse_message(application_message)
        
        user_command = int(user_command)
        
        if user_command != commands['NONE']:
            if user_command == commands['TALK']:
                print_msg(f'[{recv_user_name}]: {user_message}')
                
            elif user_command == commands['JOIN']:
                print_msg(f'{recv_user_name} joined!')
                users.add[recv_user_name] = addr[0]
                unicast(s, port, build_message('/PING', user_name), addr[0])
                
            elif user_command == commands['LEAVE']:
                print_msg(f'{recv_user_name} left!')
                users.pop(recv_user_name, None)
            
            elif user_command == commands['WHO']:
                print_msg(f'Connected users: {str(users)}')
                
            elif user_command == commands['QUIT']:
                print('Bye now!')
                terminate = True
            
            elif user_command == commands['PING']:
                users.add[recv_user_name] = addr[0]
                
            elif user_command == commands['PRIVATE-TALK']:
                print_msg(f'[{recv_user_name}] (PRIVATE): {user_message}')
                

def unicast(socket, port, message, ip_address):
    socket.sendto(message.encode(), (ip_address, port))
       
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

def print_msg(msg):
    print(f'{timestamp()} {msg}')
    
def timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    
init(sys.argv[1] if len(sys.argv) > 1 else '')
