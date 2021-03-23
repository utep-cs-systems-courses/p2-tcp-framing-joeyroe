class FramedSocket:

    #default FramedSocket constructor
    def __init__(self, socket):

        self.socket = socket

        
    #packetMaker creates the packet with the size and message
    def packetMaker(message):

        messageLength = len(message)
        packet = bytes((str(packetMaker) + ":" + message), "utf-8") #turn it into bytes
        return packet

    
    #framedSend takes a packet and sends it
    def framedSend(self, message):
        
        packet = packetMaker(message)
        self.socket.send(packet)

        
    #readMessage checks to make sure the message is correct
    def readMessage(message):

        message1 = message.decode()

        try:
            message1 = message1.split(":")
            
            if(message1[0].isdigit() == True):
                message1[0] = int(message1[0]) #turn it into an int

                if(message1[0] != len(message1[1])): #makes sure length matches
                    return None

            return message1
                
        except: #something is wrong in the message
            return None

    
