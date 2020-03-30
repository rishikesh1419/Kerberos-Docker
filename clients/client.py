import des
import socket
from datetime import datetime

def take_input() :
    uname = input("Enter username: ")
    pw = input("Enter password: ")
    #
    # create key1 using pw (DES)
    #
    key1 = "temp"
    return uname, key1

def connect_as(uname) :
    as_addr = socket.gethostname() # AS IP
    as_port = 2000 # AS Port
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((as_addr, as_port))
    clientsocket.send(uname.encode())
    packet1 = clientsocket.recv(1024).decode()
    clientsocket.send("DONE".encode())
    clientsocket.close()
    return packet1

def connect_tgs(packet1, key1) :
    #
    # decrypt packet1 using key1 (DES)
    #
    packet1 = packet1.split(",")
    c_tgs_key = packet1[0]
    ticket1 = packet1[1]
    timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    #
    # Encrypt timestamp using c_tgs_key
    #
    serverID = input("Enter serverID: ")
    #
    # Give choices
    #
    packet2 = serverID + "," + timestamp + "," + ticket1
    tgs_addr = socket.gethostname() # TGS IP
    tgs_port = 3000 # TGS Port
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((tgs_addr, tgs_port))
    clientsocket.send(packet2.encode())
    packet3 = clientsocket.recv(1024).decode()
    clientsocket.close()
    return packet3, c_tgs_key

def connect_server(packet3, c_tgs_key) :
    packet3 = packet3.split(",")
    ticket2 = packet3[0]
    ticket3 = packet3[1]
    #
    # Decrypt ticket2 using c_tgs_key to get key2 (DES)
    #
    key2 = "temp"
    timestamp = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
    #
    # Encrypt timestamp with key2 (DES)
    packet4 = timestamp + "," + ticket3
    server_addr = socket.gethostname()
    server_port = 4000
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((server_addr, server_port))
    clientsocket.send(packet4.encode())
    timestamp_enc = clientsocket.recv(1024).decode()
    #
    # Decrypt timestamp using key2 (DES)
    #
    timestamp1 = ""
    if timestamp - timestamp1 == 1 :
        return True, clientsocket, key2
    else :
        return False, clientsocket, key2

def communicate_server(clientsocket, key2) :
    text = input("Enter string: ")
    while text != "EXIT" :
        #
        # Encrypt text using key2 (DES)
        #
        clientsocket.send(text.encode())
        reply = clientsocket.recv(1024).decode()
        #
        # Decrypt reply using key2 (DES)
        #
        print("Received result:",reply)
        text = input("Enter string: ")
    clientsocket.close()



def main() :
    uname, key1 = take_input()
    packet1 = connect_as(uname)
    packet3, c_tgs_key = connect_tgs(packet1, key1)
    reply, clientsocket, key2 = connect_server(packet3, c_tgs_key)
    if reply :
        communicate_server(clientsocket, key2)
    else :
        print("Error in comminucation, try again later.")