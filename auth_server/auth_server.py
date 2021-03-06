import socket
from datetime import datetime
import redis
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import rsa
import random
import string
from time import sleep

def main() :
    r = redis.Redis()
    with open('pub_as_tgs.pem', mode='rb') as private1file:
        keydata = private1file.read()
        pub_as_tgs = rsa.PublicKey.load_pkcs1(keydata)
    word = b'cloud  computing'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    as_addr = socket.gethostname()
    as_port = 2000
    serversocket.bind((as_addr, as_port))
    serversocket.listen(5)
    print("Authentication server started.")
    while True :
        clientsocket, addr = serversocket.accept()
        print("Client connected!")
        uname = clientsocket.recv(1024)
        pw = r.get(uname.decode())
        print("Client:",uname)
        print("Password received from DB.")
        cipher = AES.new(pw, AES.MODE_ECB)
        key1 = cipher.encrypt(word)
        c_tgs_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)).encode()
        ticket1c = uname + b",,," + c_tgs_key
        ticket1 = rsa.encrypt(ticket1c, pub_as_tgs)
        # Encrypt ticket1 using public as_tgs_key (RSA)
        packet1a = c_tgs_key + b",,," + ticket1
        packet1b = pad(packet1a, 16)
        cipher = AES.new(key1, AES.MODE_ECB)
        packet1 = cipher.encrypt(packet1b)
        clientsocket.send(packet1)
        sleep(1.0)
        print("Ticket sent to the client, connection closed.",uname.decode())
        clientsocket.close()

if __name__ == '__main__' :
    main()