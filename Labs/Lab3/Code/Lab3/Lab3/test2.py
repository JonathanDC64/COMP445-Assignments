'''
Created on Mar 28, 2018

@author: Eugenio
'''
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = 'test'
clientSocket.sendto(message.encode(), ('127.0.0.1', 8080))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
