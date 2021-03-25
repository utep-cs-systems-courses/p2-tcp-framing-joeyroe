class FramedSocket:

    #default FramedSocket constructor
    def __init__(self, socket):

        self.socket = socket
    
    #framedSend takes a line from a file and creates a packet
    #with the size of the message and the actual message
    #seperated with a ':' and sends out the packet.
    def framedSend(self, fileLine):
        
        packetContent = fileLine.decode()
        packetSize = len(fileLine)
        packet = bytes((str(packetSize) + ":" + packetContent), 'utf-8') #create packet
        self.socket.send(packet)

        
    #framedReceive receives a packet and breaks the packet up from the
    #message size and actual message, it checks to make sure the message
    #size is equal to size of actual message, informs the sender if the
    #packet arrived okay or not, and finally returns message.
    def framedReceive(self):

        receivedContent = self.socket.recv(1024)
        receivedContent = receivedContent.decode().split(":")

        if(receivedContent[0].isdigit() == True): #convert str to int
            receivedContent[0] = int(receivedContent[0])

            if(receivedContent[0] == len(receivedContent[1])): #checks if the lengths match
                self.socket.send(bytes("Okay", 'utf-8')) #sends sender ACK
                return receivedContent[1] #return message

            if(receivedContent[0] != len(receivedContent[1])): #if the packet messed up
                self.socket.send(bytes("No", 'utf-8')) #lets sender know packet is bad
