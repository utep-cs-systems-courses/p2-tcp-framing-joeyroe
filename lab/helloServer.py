#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
sys.path.append("../lib")       # for params
import params
from FramedSocket import *

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets





while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it)
    
    framedSocket = FramedSocket(conn)
    
    if os.fork() == 0:      # child becomes server

        fileName = conn.recv(1024).decode() #gets fileName from client
        isFile =  os.path.isfile("serverFiles/" + fileName)

        if(isFile == False): #file doesn't exist
            conn.send(bytes("no", 'utf-8')) #sends no if the file doesn't exist 
            

        if(isFile == True): #file does exist
            conn.send(bytes("yes", 'utf-8')) #sends yes if the file exists
            conn.shutdown(socket.SHUT_WR)


        fileContent = framedSocket.framedReceive() #receive the contents from the file
        fd = os.open("serverFiles/" + fileName, os.O_CREAT | os.O_WRONLY) #create the file
        os.write(fd, fileContent.encode())
        os.close(fd)
        
