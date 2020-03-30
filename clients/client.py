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
    tgs_port = 2000 # TGS Port
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((tgs_addr, tgs_port))
    clientsocket.send(packet2.encode())
    packet3 = clientsocket.recv(1024).decode()
    return packet3, c_tgs_key

def connect_server(packet3, c_tgs_key) :
    packet3 = packet3.split(",")
    ticket2 = packet3[0]
    ticket3 = packet3[1]
    #
    # Decrypt ticket2 using c_tgs_key (DES)
    #
    


def main() :
    uname, key1 = take_input()
    packet1 = connect_as(uname)
    packet3, c_tgs_key = connect_tgs(packet1, key1)
    connect_server(packet3, c_tgs_key)