import datetime
import sys
import threading
import socket

start()

chn = 'general'
BROADCAST = '255.255.255.255'

def receiver(username, ip, port):
    global users
    global chn
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip,port))
    BUFFER = 2048
    while True:
        formatted_message, addr = s.recvfrom(BUFFER)
        (msg_username, cmd, channel, msg) = parse_message(formatted_message)
        time = datetime.now().strftime("%H:%M:%S")
        if cmd == 'talk' and channel == chn:
            print(time + ' [' + msg_username + ' #' + chn + ']: ' + msg)
        elif cmd == 'who':
            print(time + ' list of connected users: ' + str(users.keys()))            
        elif cmd == 'quit':
            print('Bye now!')
            quit()
        elif cmd == 'join':
            if msg_username not in users.keys():
                print(time + ' ' + msg_username + ' joined the chat room.')    
                send_to_one(s, port, build_message('/ping', username, chn), addr[0])
                users[msg_username] = addr[0]
            else:
                send_to_one(s, port, build_message('/duplicate', username, chn), addr[0])   
        elif cmd == 'leave':
            print(time + ' ' + msg_username + ' left the chat room.')
            users.pop(msg_username, None)
        elif cmd == 'private':
            print(time + ' [' + msg_username + '] (PRIVATE): ' + msg)       
        elif cmd == 'ping':
            users[msg_username] = addr[0]
        elif cmd == 'channel':
            chn = msg
            print(time + ' Switching channel to ' + chn)
        elif cmd == 'duplicate':
            print('Username already exists.')

def sender(username, ip, port):
    global chn
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    joined = False
    while True:
        if not joined:
            formatted_message = build_message('/join', username, chn)
            send_to_all(s, port, formatted_message)
            joined = True       
        message = input('')        
        formatted_message = build_message(message, username, chn)        
        msg = ''
        cmd = ''
        if message[0] == '/': 
            if message.find(' ') > 0:
                msg = message[message.find(' ')+1:]
                cmd = message[1:message.find(' ')]
            else:
                cmd = message[1:]
        else:
            cmd =  'talk'        
        if cmd == 'channel':
            send_to_one(s, port, formatted_message, ip)
        elif cmd == 'private':
            send_to_one(s, port, build_message('/private ' + ' '.join(msg.split(' ')[1:]), username, chn), users[msg.split(' ')[0]])
        elif cmd == 'leave':
            send_to_all(s, port, formatted_message)
            send_to_one(s, port, build_message('/quit', username, chn), ip)           
        elif cmd == 'who':
            send_to_one(s, port, formatted_message, ip)        
        else:
            send_to_all(s, port, formatted_message)
                    
def build_message(message, user_name, user_channel='general'):
    command = ''
    if message[0] == '/': 
        if message.find(' ') > 0:
            message = msg[message.find(' ')+1:]
            command = msg[1:message.find(' ')]
        else:
            command = msg[1:]
    else:
        command =  'talk'
    return 'user:' + user_name + '\ncommand:' + cmd + '\nchannel:' + user_channel +'\nmessage:' + msg + '\n\n'

def parse_message(formatted_message):
    seperations = formatted_message.decode().split('\n')
    return seperations[0].split(':')[1], seperations[1].split(':')[1], seperations[2].split(':')[1], seperations[3].split(':')[1]
    
def send_to_all(s, port, msg):
    msg = msg.encode()
    addr = (BROADCAST, port)
    s.sendto(msg, addr)

def send_to_one(s, port, msg, ip):
    msg = msg.encode()
    addr = (ip, port)
    s.sendto(msg, addr)

users = None       
def start(ip = '', port = 1337):
    global users
    users = {}
    username = input('Please enter your name: ')
    sender_thread = threading.Thread(target=sender, args=(username, ip, port))
    receiver_thread = threading.Thread(target=receiver, args=(username, ip, port))
    sender_thread.start()
    receiver_thread.start()




