import socket
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import rsa
import random
import string

def main() :
    with open('pub_tgs_server.pem', mode='rb') as private1file:
        keydata = private1file.read()
        pub_tgs_server = rsa.PublicKey.load_pkcs1(keydata)
    with open('pri_as_tgs.pem', mode='rb') as private1file:
        keydata = private1file.read()
        pri_as_tgs = rsa.PrivateKey.load_pkcs1(keydata)
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tgs_addr = socket.gethostname()
    tgs_port = 3000
    serversocket.bind((tgs_addr, tgs_port))
    while True :
        serversocket.listen(5)
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        packet2 = clientsocket.recv(1024)
        packet2 = packet2.split(b",,,")
        if len(packet2) != 3 :
            # do something
            print("error")
        else :
            serverID = packet2[0]
            ticket1b = packet2[2]
            timestamp = packet2[1]
            # Decrypt ticket1 using private as_tgs_key (RSA)
            ticket1a = rsa.decrypt(ticket1b, pri_as_tgs)
            ticket1 = ticket1a.split(b",,,")
            if len(ticket1) != 2 :
                # do something
                print("error")
            else :
                uname = ticket1[0]
                c_tgs_key = ticket1[1]
                cipher = AES.new(c_tgs_key, AES.MODE_ECB)
                timestamp1 = cipher.decrypt(timestamp)
                timestamp1a = unpad(timestamp1, 16)
                timestamp1b = datetime.strptime(timestamp1a.decode(), "%Y-%m-%d %H:%M:%S.%f")
                timestamp = datetime.utcnow()
                # Check timestamp validity
                # if invalid
                if (timestamp - timestamp1b).seconds > 60 :
                    # do something
                    print("error")
                else :
                    key2 = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)).encode()
                    ticket2a = serverID + b",,," + key2
                    ticket2b = pad(ticket2a, 16)
                    ticket2 = cipher.encrypt(ticket2b)
                    ticket3a = uname + b",,," + key2
                    # Encrypt ticket3 using public tgs_server_key (RSA)
                    ticket3 = rsa.encrypt(ticket3a, pub_tgs_server)
                    packet3 = ticket2 + b",,," + ticket3
                    clientsocket.send(packet3)
                    print("Tickets send to client,",uname.decode())
                    clientsocket.close()

if __name__ == '__main__' :
    main()