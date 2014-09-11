# import socket
# import sys
 
# HOST = 'localhost'   # Symbolic name, meaning all available interfaces
# PORT = 40000 # Arbitrary non-privileged port
 
# s = socket.socket(socket.IPPROTO_TCP, socket.TCP_NODELAY)
# print 'Socket created'
 
# #Bind socket to local host and port
# try:
#     s.bind((HOST, PORT))
# except socket.error as msg:
#     print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#     sys.exit()
     
# print 'Socket bind complete'
 
# #Start listening on socket
# s.listen(10)
# print 'Socket now listening'
 
# #now keep talking with the client
# while 1:
#     #wait to accept a connection - blocking call
#     conn, addr = s.accept()
#     print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
# s.close()



#!/usr/bin/env python
    
import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 40000
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
   data = conn.recv(BUFFER_SIZE)
   if not data: break
   print "received data:", data
   conn.send(data)  # echo
conn.close()