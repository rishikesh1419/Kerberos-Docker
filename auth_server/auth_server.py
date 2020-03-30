import socket
import des
from datetime import datetime

# 
# Hardcoding password
# Connect to redis db later
#

def main() :
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    as_addr = socket.gethostname()
    as_port = 2000
    serversocket.bind((as_addr, as_port))
    while True :
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        uname = clientsocket.recv(1024).decode()
        #
        # get pw from DB
        # create key1 using pw (DES)
        #
        print("Client:",uname)
        key1 = "temp"
        #
        # Generate c_tgs_key
        #
        c_tgs_key = "temp"
        ticket1 = uname + "," + c_tgs_key
        #
        # Encrypt ticket1 using public as_tgs_key (RSA)
        #
        packet1 = c_tgs_key + "," + ticket1
        #
        # Encrypt packet1 with key1 (DES)
        #
        clientsocket.send(packet1.encode())
        print("Ticket sent to client",uanme)
        clientsocket.close()