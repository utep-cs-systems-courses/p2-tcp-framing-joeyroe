
#! /usr/bin/env python3

# Echo client program
import socket, sys, re, time
sys.path.append("../lib")       # for params
import params
import os
from FramedSocket import *

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(delay)
    print("done sleeping")





#client first sends the name of the file, the server checks to see if 
#the file already exists in the directory with replying with a yes if it
#does and no if it doesn't. If the file doesn't exist the client sends the
#file contents to the server using a framed socket.


fileName = input() 
framedSocket = FramedSocket(s)

s.send(bytes(fileName, 'utf-8')) #just sends the name of the file to the server
fileExists = s.recv(1024).decode() #server response to if file already exists or not

fd = os.open(fileName, os.O_RDONLY)

if(fileExists == 'no'):

    fd = os.open(fileName, os.O_RDONLY)
    #a = os.read(fd, 200)
    #framedSocket.framedSend(a)
    
    fileContents = ""
        
    while(True):

        contentRead = os.read(fd, 200) #read 200 bytes at a time from fd

        print(contentRead)

        if(len(contentRead) == 0): #finished reading the file breaks from the while loop
            break

        fileContents += contentRead.decode() #groups content of the file together

    framedSocket.framedSend(bytes(fileContents, 'utf-8')) #sends file contents
    s.close()
    print("sent file ", fileName, " to the server")

if(fileExists == 'yes'): #server already has file with that name

    print("file already exists")
    sys.exit(1)


