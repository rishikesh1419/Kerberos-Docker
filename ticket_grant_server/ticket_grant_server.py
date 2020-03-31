import socket
from datetime import datetime
import des

def main() :
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tgs_addr = socket.gethostname()
    tgs_port = 3000
    serversocket.bind((tgs_addr, tgs_port))
    while True :
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        packet2 = clientsocket.recv(1024).decode()
        packet2 = packet2.split(",,,")
        if len(packet2) != 3 :
            # do something
        else :
            serverID = packet2[0]
            ticket1 = packet[2]
            timestamp = packet2[1]
            #
            # Decrypt ticket1 using private as_tgs_key (RSA)
            #
            ticket1 = ticket1.split(",,,")
            if len(ticket1) != 2 :
                # do something
            else :
                uname = ticket1[0]
                c_tgs_key = ticket1[1]
                #
                # Decrypt timestamp using c_tgs_key (DES)
                # Check timestamp validity
                #
                # if invalid
                if False :
                    # do something
                else :
                    #
                    # generate client-server-session-key key2 (DES)
                    #
                    key2 = "temp"
                    ticket2 = serverID + ",,," + key2
                    #
                    # Encrypt ticket2 using c_tgs_key (DES)
                    #
                    ticket3 = uname + ",,," + key2
                    #
                    # Encrypt ticket3 using public tgs_server_key (RSA)
                    #
                    packet3 = ticket2 + ",,," + ticket3
                    clientsocket.send(packet3)
                    print("Tickets send to client,"uname)
                    clientsocket.close()