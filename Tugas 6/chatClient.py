import socket
import json
import base64
import json
import os
TARGET_IP = "172.16.16.101"
TARGET_PORT = 8889

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (TARGET_IP,TARGET_PORT)
        self.sock.connect(self.server_address)
        self.tokenid=""
    def proses(self,cmdline):
        j=cmdline.split(" ")
        try:
            command=j[0].strip()
            if (command=='auth'):
                username=j[1].strip()
                password=j[2].strip()
                return self.login(username,password)
            if (command=='register'):
                username=j[1].strip()
                password=j[2].strip()
                negara=j[3].strip()
                nama=j[4:]
                return self.register(username, password, negara, nama)
            elif (command=='addrealm'):
                realmid = j[1].strip()
                realm_address = j[2].strip()
                realm_port = j[3].strip()
                return self.add_realm(realmid, realm_address, realm_port)
            elif (command=='addgroup'):
                groupname = j[1].strip()
                return self.add_group(groupname)
            elif (command=='joingroup'):
                groupname = j[1].strip()
                return self.join_group(groupname)
            elif (command=='send'):
                usernameto = j[1].strip()
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message,w)
                return self.send_message(usernameto,message)
            elif (command=='sendfile'):
                usernameto = j[1].strip()
                filepath = j[2].strip()
                return self.send_file(usernameto,filepath)
            elif (command=='sendgroup'):
                groupname = j[1].strip()
                message=""
                for w in j[2:]:
                    message="{} {}" . format(message,w)
                return self.send_group_message(groupname,message)
            elif (command=='sendgroupfile'):
                groupname = j[1].strip()
                filepath = j[2].strip()
                return self.send_group_file(groupname,filepath)
            elif (command == 'sendprivaterealm'):
                realmid = j[1].strip()
                username_to = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                return self.send_realm_message(realmid, username_to, message)
            elif (command=='sendfilerealm'):
                realmid = j[1].strip()
                usernameto = j[2].strip()
                filepath = j[3].strip()
                return self.send_file_realm(realmid, usernameto,filepath)
            elif (command=='sendgrouprealm'):
                realmid = j[1].strip()
                usernamesto = j[2].strip()
                message=""
                for w in j[3:]:
                    message="{} {}" . format(message,w)
                return self.send_group_realm_message(realmid, usernamesto,message)
            elif (command=='sendgroupfilerealm'):
                realmid = j[1].strip()
                usernamesto = j[2].strip()
                filepath = j[3].strip()
                return self.send_group_file_realm(realmid, usernamesto,filepath)
            elif (command=='inbox'):
                return self.inbox()
            elif (command=='privateinbox'):
                username=""
                username = j[1].strip()
                return self.privateinbox(username)
            elif (command=='groupinbox'):
                groupname=""
                groupname = j[1].strip()
                return self.groupinbox(groupname)
            elif (command == 'getrealminbox'):
                realmid = j[1].strip()
                return self.realm_inbox(realmid)
            elif (command=='logout'):
                return self.logout()
            elif (command=='info'):
                return self.info()
            elif (command=='getusers'):
                return self.getusers()
            elif (command=='getgroups'):
                return self.getgroups()
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"

    def sendstring(self,string):
        try:
            self.sock.sendall(string.encode())
            receivemsg = ""
            while True:
                data = self.sock.recv(1024)
                # print("diterima dari server",data)
                if (data):
                    receivemsg = "{}{}" . format(receivemsg,data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
                    if receivemsg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(receivemsg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}

    def login(self,username,password):
        string="auth {} {} \r\n" . format(username,password)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return "OK | {} | {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])
    
    def register(self,username,password, negara, nama):
        nama=' '.join(str(e) for e in nama)
        string="register {} {} {} {}\r\n" . format(username,password, negara, nama)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=result['tokenid']
            return " {} {} " .format(username,self.tokenid)
        else:
            return "Error, {}" . format(result['message'])

    def getusers(self):
        result = self.sendstring("getusers \r\n")
        if result['status']=='OK':
            return result['users']
        else:
            return "Error, {}" . format(result['message'])

    def getgroups(self):
        result = self.sendstring("getgroups \r\n")
        if result['status']=='OK':
            return result
        else:
            return "Error, {}" . format(result['message'])

    def add_realm(self, realmid, realm_address, realm_port):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="addrealm {} {} {} \r\n" . format(realmid, realm_address, realm_port)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "Realm {} added" . format(realmid)
        else:
            return "Error, {}" . format(result['message'])

    def add_group(self, groupname):
        string="addgroup {} {} \r\n".format(self.tokenid, groupname)
        result = self.sendstring(string)
        return "{}".format(result['message'])
    
    def join_group(self, groupname):
        string="joingroup {} {} \r\n".format(self.tokenid, groupname)
        result = self.sendstring(string)
        return "{}".format(result['message'])

    def send_message(self,usernameto="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
        print(string)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(usernameto)
        else:
            return "Error, {}" . format(result['message'])
        
    def send_file(self, usernameto="xxx", filepath="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"

        if not os.path.exists(filepath):
            return {'status': 'ERROR', 'message': 'File not found'}
        
        with open(filepath, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)  # Decode byte-string to UTF-8 string
        string="sendfile {} {} {} {}\r\n" . format(self.tokenid,usernameto,filepath,encoded_content)

        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(result['address'])
        else:
            return "Error, {}" . format(result['message'])

    def send_realm_message(self, realmid, username_to, message):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="sendprivaterealm {} {} {} {}\r\n" . format(self.tokenid, realmid, username_to, message)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "Message sent to realm {}".format(realmid)
        else:
            return "Error, {}".format(result['message'])
        
    def send_file_realm(self, realmid, usernameto, filepath):
        if (self.tokenid==""):
            return "Error, not authorized"
        if not os.path.exists(filepath):
            return {'status': 'ERROR', 'message': 'File not found'}
        
        with open(filepath, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)  # Decode byte-string to UTF-8 string
        string="sendfilerealm {} {} {} {} {}\r\n" . format(self.tokenid, realmid, usernameto, filepath, encoded_content)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "File sent to realm {}".format(realmid)
        else:
            return "Error, {}".format(result['message'])

    def send_group_message(self,groupname="xxx",message="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="sendgroup {} {} {} \r\n" . format(self.tokenid,groupname,message)
        print(string)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to {}" . format(groupname)
        else:
            return "Error, {}" . format(result['message'])
        
    def send_group_file(self, groupname="xxx", filepath="xxx"):
        if (self.tokenid==""):
            return "Error, not authorized"
        
        if not os.path.exists(filepath):
            return {'status': 'ERROR', 'message': 'File not found'}
        
        with open(filepath, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)  # Decode byte-string to UTF-8 string

        string="sendgroupfile {} {} {} {}\r\n" . format(self.tokenid,groupname,filepath, encoded_content)

        result = self.sendstring(string)
        if result['status']=='OK':
            return "file sent to {}" . format(groupname)
        else:
            return "Error, {}" . format(result['message'])

    def send_group_realm_message(self, realmid, usernames_to, message):
        if self.tokenid=="":
            return "Error, not authorized"
        string="sendgrouprealm {} {} {} {} \r\n" . format(self.tokenid, realmid, usernames_to, message)

        result = self.sendstring(string)
        if result['status']=='OK':
            return "message sent to group {} in realm {}" .format(usernames_to, realmid)
        else:
            return "Error {}".format(result['message'])
        
    def send_group_file_realm(self, realmid, usernames_to, filepath):
        if self.tokenid=="":
            return "Error, not authorized"

        if not os.path.exists(filepath):
            return {'status': 'ERROR', 'message': 'File not found'}
        
        with open(filepath, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content)  # Decode byte-string to UTF-8 string
        string="sendgroupfilerealm {} {} {} {} {}\r\n" . format(self.tokenid, realmid, usernames_to, filepath, encoded_content)

        result = self.sendstring(string)
        if result['status']=='OK':
            return "file sent to group {} in realm {}" .format(usernames_to, realmid)
        else:
            return "Error {}".format(result['message'])

    def privateinbox(self, username):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="privateinbox {} {} \r\n" . format(self.tokenid, username)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

    def inbox(self):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="inbox {} \r\n" . format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])

    def realm_inbox(self, realmid):
        if (self.tokenid==""):
            return "Error, not authorized"
        string="getrealminbox {} {} \r\n" . format(self.tokenid, realmid)
        print("Sending: " + string)
        result = self.sendstring(string)
        if result['status']=='OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}".format(result['message'])
    
    def logout(self):
        string="logout {}\r\n".format(self.tokenid)
        result = self.sendstring(string)
        if result['status']=='OK':
            self.tokenid=""
            return "Logout Berhasil"
        else:
            return "Error, {}" . format(result['message'])

    def info(self):
        string="info \r\n"
        result = self.sendstring(string)
        list_user_aktif="User yang Aktif:\n"
        if result['status']=='OK':
            list_user_aktif += f"{result['message']}"
        return list_user_aktif

if __name__=="__main__":
    cc = ChatClient()
    while True:
        print("\n")
        print("""Command:\n
        Inter-Realm Command\n
        1. Login: auth [username] [password]
        2. Register: register [username] [password] [negara] [nama]
        3. Buat grup: addgroup [nama_group]
        4. Join grup: joingroup [nama_group]
        5. Mengirim pesan: send [username to] [message]
        6. Mengirim file: sendfile [username to] [filename]
        7. Mengirim pesan ke group: sendgroup [nama_group] [message]
        8. Mengirim file ke group: sendgroupfile [nama_group] [filename]
        9. Melihat pesan: inbox
        10. Logout: logout
        11. Melihat user yang aktif: info
        
        Multi-Realm Command:\n
        1. Menambah realm: addrealm [nama_realm] [address] [port]
        2. Mengirim pesan ke realm: sendprivaterealm [name_realm] [username to] [message]
        3. Mengirim file ke realm: sendfilerealm [name_realm] [username to] [filename]
        4. Mengirim pesan ke group realm: sendgrouprealm [name_realm] [nama_group] [message]
        5. Mengirim file ke group realm: sendgroupfilerealm [name_realm] [nama_group] [filename]
        6. Melihat pesan dari realm: getrealminbox [nama_realm]""")
        
        cmdline = input("Command {}:" . format(cc.tokenid))
        print(cc.proses(cmdline))