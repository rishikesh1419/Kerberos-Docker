import socket
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def main() :
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
        else :
            serverID = packet2[0]
            ticket1 = packet[2]
            timestamp = packet2[1]
            #
            # Decrypt ticket1 using private as_tgs_key (RSA)
            #
            ticket1 = ticket1.split(b",,,")
            if len(ticket1) != 2 :
                # do something
            else :
                uname = ticket1[0]
                c_tgs_key = ticket1[1]
                cipher = AES.new(c_tgs_key, AES.MODE_ECB)
                timestamp1 = cipher.decrypt(timestamp)
                timestamp1a = unpad(timestamp1, 16)
                #
                # 
                # Check timestamp validity
                #
                # if invalid
                if False :
                    # do something
                else :
                    key2 = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)).encode()
                    ticket2a = serverID + b",,," + key2
                    ticket2b = pad(ticket2a, 16)
                    ticket2 = cipher2.encrypt(ticket2b)
                    ticket3 = uname + b",,," + key2
                    #
                    # Encrypt ticket3 using public tgs_server_key (RSA)
                    #
                    packet3 = ticket2 + b",,," + ticket3
                    clientsocket.send(packet3)
                    print("Tickets send to client,"uname.decode())
                    clientsocket.close()