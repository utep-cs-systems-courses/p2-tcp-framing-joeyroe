import os
import threading
from threading import Thread
from FramedSocket import *

threadNum = 0
inTransfer = set()
transferLock = threading.Lock()

class Worker(Thread):
    
    def __init__(self, connectedSock, addr):

        global threadNum
        Thread.__init__(self, name = "Thread-%d" % threadNum)
        threadNum += 1
        self.connectedSock = connectedSock
        self.addr = addr

    #transferCheck checks to see if the fileName
    #is in the set "inTransfer" if in the set
    #False is returned, if not the fileName is
    #added and True is retruned
    def transferCheck(self, fileName):

        global inTransfer
        global transferLock
        transferLock.acquire()
        isTransfer = False

        if(fileName not in inTransfer):
            isTransfer = True
            inTransfer.add(fileName)

        transferLock.release()

        return isTransfer

    #removes fileName from set
    def endTransfer(self, fileName):
        global inTransfer
        inTransfer.remove(fileName)


    #run carries out the actions of the server
    #it receives the a message from the client on
    #whether or not the file is in a directroy "serverFiles"
    #then it receives the contents of the file and creates
    #a new file in the directory "serverFiles"
    def run(self):

        fileName = self.connectedSock.recv(1024).decode() #gets the name of the file
        framedSocket = FramedSocket(self.connectedSock)
        isTransfer = self.transferCheck(fileName)

        if(isTransfer == True): #if the file is in the set "inTransfer"

            if(os.path.isfile("serverFiles/" + fileName) == False): #if file isn't in directory
                self.connectedSock.send(bytes("no", 'utf-8'))

            if(os.path.isfile("serverFiles/" + fileName) == True): #if file is in directory
                self.connectedSock.send(bytes("yes", 'utf-8'))
                connectedSock.shutdown(socket.SHUT_WR)
                
        if(isTransfer == False): #file not in the seet
            print("can not transfer file")

        fileContent = framedSocket.framedReceive()
        fd = os.open("serverFiles/" + fileName, os.O_CREAT | os.O_WRONLY)
        os.write(fd, fileContent.encode())
        print("File is now in serverFiles")
        os.close(fd)
