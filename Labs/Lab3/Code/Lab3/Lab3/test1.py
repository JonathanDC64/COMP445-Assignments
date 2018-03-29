'''
Created on Mar 28, 2018

@author: Eugenio
'''
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('',8080))
while True:
    message, clientAddress = s.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    s.sendto(modifiedMessage.encode(),clientAddress)
