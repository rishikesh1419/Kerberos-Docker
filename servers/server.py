import des
import socket
from datetime import datetime

def check(clientsocket) :
    #
    # RETURN FALSE ???????
    #
    packet4 = clientsocket.recv(1024).decode()
    packet4 = packet4.split(",")
    if len(packet4) != 2 :
        # do something
    else :
        timestamp = packet4[0]
        ticket3 = packet4[1]
        #
        # Decrypt ticket3 using private as_tgs_key (RSA)
        #
        ticket3 = ticket3.split(",")
        if len(ticket3) != 2 :
            # do something
        else :
            uname = ticket3[0]
            key2 = ticket3[1]
            #
            # Decrypt timestamp using key2 (DES)
            # if timestamp is invalid
            if False :
                # do something
                return False, "", ""
            else :
                #
                # timestamp1 = timestamp - 1
                timestamp1 = "temp"
                #
                # Encrypt timestamp1 using key2 (DES)
                #
                clientsocket.send(timestamp1.encode())
                #
                # Insert (serverID, uname, timestampSelf) to DB
                #
                return True, uname, key2
                    

def serve(clientsocket, uname, key2) :
    while True :
        #
        # Check timestamp validity from DB
        #if invalid
        if False:
            # do something, remove from DB, etc...
        else :
            packet5 = clientsocket.recv(1024).decode()
            #
            # Decrypt packet5 using key2 (DES)
            # Process packet5 text
            result = "temp"
            # 
            # Encrypt result using key2 (DES)
            #
            clientsocket.send(result.encode())







def main() :
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_addr = socket.gethostname()
    srv_port = 4000
    serversocket.bind((srv_addr, srv_port))
    while True :
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        result, uname, key2 = check(clientsocket)
        if result :
            serve(clientsocket, key2)
        else :
            clientsocket.close()
            # ??????
