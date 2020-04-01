import socket
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
import time

def take_input() :
    uname = input("Enter username: ")
    pw = input("Enter your 16-digit password: ").encode()
    word = b'cloud  computing'
    cipher = AES.new(pw, AES.MODE_ECB)
    key1 = cipher.encrypt(word)
    return uname, key1

def connect_as(uname) :
    as_addr = socket.gethostname() # AS IP
    as_port = 2000 # AS Port
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((as_addr, as_port))
    clientsocket.send(uname.encode())
    packet1 = clientsocket.recv(1024)
    clientsocket.send("DONE".encode())
    clientsocket.close()
    return packet1

def connect_tgs(packet1a, key1) :
    cipher = AES.new(key1, AES.MODE_ECB)
    packet1b = cipher.decrypt(packet1a)
    print(packet1b)
    packet1 = unpad(packet1b, 16)
    packet1 = packet1.split(b",,,")
    if len(packet1) != 2 :
        print("Invalid credentials 1!")
        exit(0)
    # check exit(0)
    c_tgs_key = packet1[0]
    ticket1 = packet1[1]
    timestamp1 = str(datetime.utcnow()).encode()
    # TIMESTAMP FORMAT
    cipher2 = AES.new(c_tgs_key, AES.MODE_ECB)
    timestamp1a = pad(timestamp1, 16)
    timestamp = cipher2.encrypt(timestamp1a)
    serverID = input("Enter serverID: ").encode()
    #
    # Give choices
    #
    packet2 = serverID + b",,," + timestamp + b",,," + ticket1
    tgs_addr = socket.gethostname() # TGS IP
    tgs_port = 3000 # TGS Port
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((tgs_addr, tgs_port))
    clientsocket.send(packet2)
    packet3 = clientsocket.recv(1024)
    # clientsocket.close()
    return packet3, c_tgs_key

def connect_server(packet3, c_tgs_key) :
    print("Inside connect_server")
    packet3 = packet3.split(b",,,")
    if len(packet3) != 2 :
        print("Invalid credentials 2!")
        exit(0)
        # check exit(0)
    ticket2 = packet3[0]
    ticket3 = packet3[1]
    cipher = AES.new(c_tgs_key, AES.MODE_ECB)
    ticket2a = cipher.decrypt(ticket2)
    ticket2b = unpad(ticket2a, 16)
    ticket2c = ticket2b.split(b",,,")
    key2 = ticket2c[1]
    timestamp1 = str(datetime.utcnow()).encode()
    # TIMESTAMP FORMAT
    cipher2 = AES.new(key2, AES.MODE_ECB)
    timestamp1a = pad(timestamp1, 16)
    timestamp = cipher2.encrypt(timestamp1a)
    packet4 = timestamp + b",,," + ticket3
    server_addr = socket.gethostname()
    server_port = 4000
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((server_addr, server_port))
    clientsocket.send(packet4)
    timestamp_enc = clientsocket.recv(1024)
    timestamp2a = cipher2.decrypt(timestamp_enc)
    timestamp2b = unpad(timestamp2a, 16)
    timestamp2 = datetime.strptime(timestamp2b.decode(), "%Y-%m-%d %H:%M:%S.%f")
    # TIMESTAMP FORMAT
    timestamp1 = datetime.strptime(timestamp1.decode(), "%Y-%m-%d %H:%M:%S.%f")
    if (timestamp1 - timestamp2).seconds == 1 :
        return "True", clientsocket, key2
    else :
        return "False", clientsocket, key2

def communicate_server(clientsocket, key2) :
    text = input("Enter string: ").encode()
    while text != b"EXIT" :

        cipher = AES.new(key2, AES.MODE_ECB)
        text1 = pad(text, 16)
        text1a = cipher.encrypt(text1)
        clientsocket.send(text1a)
        reply1a = clientsocket.recv(1024)
        reply1 = cipher.decrypt(reply1a)
        reply = unpad(reply1, 16)

        print("Received result:",reply.decode())
        text = input("Enter string: ").encode()
    clientsocket.close()



def main() :
    uname, key1 = take_input()
    packet1 = connect_as(uname)
    packet3, c_tgs_key = connect_tgs(packet1, key1)
    reply, clientsocket, key2 = connect_server(packet3, c_tgs_key)
    if reply == "True" :
        communicate_server(clientsocket, key2)
    else :
        print("Error in comminucation, try again later.")

if __name__ == '__main__' :
    main()