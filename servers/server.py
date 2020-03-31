import socket
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def check(clientsocket) :
    #
    # RETURN FALSE ???????
    #
    packet4 = clientsocket.recv(1024)
    packet4 = packet4.split(b",,,")
    if len(packet4) != 2 :
        # do something
    else :
        timestamp = packet4[0]
        ticket3 = packet4[1]
        #
        # Decrypt ticket3 using private as_tgs_key (RSA)
        #
        ticket3 = ticket3.split(b",,,")
        if len(ticket3) != 2 :
            # do something
        else :
            uname = ticket3[0]
            key2 = ticket3[1]
            cipher2 = AES.new(key2, AES.MODE_ECB)
            timestamp1 = cipher2.decrypt(timestamp)
            timestamp1a = unpad(timestamp1, 16)
            #
            # TIMESTAMP FORMAT
            # if timestamp is invalid
            #
            if False :
                # do something
                return False, b"", b""
            else :
                #
                # timestamp1 = timestamp - 1
                # TIMESTAMP FORMAT
                timestamp1b = b"temp"
                timestamp1a = pad(timestamp1b, 16)
                timestamp1 = cipher2.encrypt(timestamp1a)
                clientsocket.send(timestamp1.encode())
                return True, uname, key2
                    

def serve(clientsocket, uname, key2) :
    #
    # Start timer
    #
    while True :
        #
        # Check timer
        # if invalid
        #
        if False:
            # do something, send msg, etc...
            clientsocket.close()
        else :
            packetb = clientsocket.recv(1024)
            cipher2 = AES.new(key2, AES.MODE_ECB)
            packet5a = cipher2.decrypt(packet5b)
            packet5 = unpad(packet5a, 16)
            #
            # Process packet5 text
            #
            result1a = b"temp"
            result1 = pad(result1a, 16)
            result = cipher2.encrypt(result1)
            clientsocket.send(result)







def main() :
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_addr = socket.gethostname()
    srv_port = 4000
    serversocket.bind((srv_addr, srv_port))
    serversocket.listen(5)
    while True :
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        result, uname, key2 = check(clientsocket)
        if result :
            serve(clientsocket, key2)
        else :
            clientsocket.close()
            # ??????
