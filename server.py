__author__ = "F-162A7V"

import socket, struct, threading, pickle, random
import smtplib, ssl, time
from email.message import EmailMessage
import senderobject
from hashlib import sha256
from email_validator import validate_email


users = {}
diction = senderobject.Sender()
stop = False
pepper = "A4-D#8K.;"
threads = []


def makeSendableMSG(msg):
    length = struct.pack("I",len(msg))
    return length + msg.encode()

def recieveData(sock):
    resp = sock.recv(4)
    recvlen = struct.unpack("I",resp)
    resp = sock.recv(recvlen)
    return resp, resp.split(b'|``|')



def hash_pass(password,salt):
    global pepper
    password = password + salt + pepper
    return sha256(password.encode()).hexdigest()


def send_email(email_reciever,email_subject,email_body):
    email_sender = "yoavsarig4@gmail.com"
    email_password = 'rceb pwyw jfey ccrh'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = email_subject
    em.set_content()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciever,em.as_string())


def findUsernameByEmail(email):
    global users
    for key in users:
        if users[key][1] == email:
            return key

    return "-1"


def ResetCodeTimer(username,notuple):
    global users, stop
    t1 = time.perf_counter()
    while not stop:
        t2 = time.perf_counter()
        if t2 - t1 > 300:
            users[username][3] = False


def passchangesequence(sock,tgtemail):
    global users, pepper, threads
    tgt_user = findUsernameByEmail(tgtemail)
    try:
        if validate_email(tgtemail) and users[tgt_user][1].decode() == tgtemail:
            msg = "FGTR"
            msg = makeSendableMSG(msg)
            code = str(random.randint(1,999999)).zfill(6)
            send_email(tgtemail,"AsyncServerGui password reset code:", code)
            sock.send(msg)
            tn = threading.Thread(target=ResetCodeTimer,args=(tgt_user,""))
            tn.start()
            threads.append(tn)
            users[tgt_user][3] = True
            data, fields = recieveData(sock)
            if fields[0] == b'FPCD':
                if fields[1].decode == code:
                    msg = makeSendableMSG('FPCR')
                    sock.send(msg)
                    data, fields2 = recieveData(sock)
                    if fields2[0] == 'NEWP':
                        new_pass = fields2[1]
                        salt = users[tgt_user][2]
                        users[tgt_user][0] = hash_pass(new_pass,salt)
                        msg = makeSendableMSG('NEWR')
                    else:
                        msg = makeSendableMSG("EROR|005")
                        sock.send(msg)
                else:
                    msg = makeSendableMSG('EROR|008')
                    sock.send(msg)
            else:
                msg = makeSendableMSG('EROR|005')
                sock.send(msg)
        else:
           sock.send(makeSendableMSG('EROR|009'))
    except:
        pass



def handl_cli(sock,user):
    global stop, diction
    while not stop:
        len = sock.recv(4)
        if len == b'':
            break
        len = struct.unpack("I",len)[0]
        data = sock.recv(len)
        if data == b'':
            break
        data = data.decode()
        fields = data.split('|``|')
        print(data)
        parse_msg(fields,sock)


def parse_msg(fields,sock):
    global diction
    global pepper
    try:
        code = fields[0]
        msg = ''
        if code == 'SIGN':
            email = fields[1]
            username = fields[2]
            noenc_password = fields[3]
            if username not in users:
                salt = sha256(str(random.randint(0,10000000)).encode()).hexdigest()[:6]
                password = noenc_password + salt + pepper
                login_underway = False
                users[username] = [sha256(password.encode()).hexdigest(),email,salt,login_underway]
                diction.socksender[username] = []
                with open("users.pkl", "wb") as fil:
                    pickle.dump(users, fil)
                msg = 'SIGR|``|T'
            else:
                msg = 'EROR|``|004'

        if code == "LOGN":
            username = fields[1]
            noenc_password = fields[2]
            if username in users:
                password = noenc_password + users[username][2] + pepper
                enc = sha256(password.encode()).hexdigest()
                if users[username][0] == enc:
                        msg = "LOGR"
                else:
                    msg = "EROR|``|002"
            else:
                msg = "EROR|``|002"

        if code == "FGTP":
            passchangesequence(sock,fields[1])

        if code == "MESG":
            keys = diction.socksender.keys()
            if fields[2] in keys:
                msg = f'MESS|``|{fields[1]}|``|{fields[3]}'
            else:
                msg = "EROR|``|003"
    except IndexError:
        msg = "EROR|``|005"
    length = struct.pack("I",len(msg))
    msg = length + msg.encode()
    if msg[:4] == "MESS":
        print(msg)
        diction.AddMsg(fields[2],msg)
        with open("messages.pkl", "wb") as fil:
            pickle.dump(diction.socksender, fil)
    else:
        try:
            print(msg)
            sock.send(msg)
        except:
            pass


def mgsDispatcher():
    global diction
    global stop
    while not stop:
        for t in diction.socksender:
            for x in t:
                try:
                    msg = t[x]
                    if msg != b'':
                        diction.sock_by_name[t].send(msg)
                    with open("messages.pkl", "wb") as fil:
                        pickle.dump(diction.socksender, fil)
                except:
                    pass


def main(ip,port):
    global diction
    global users
    global stop
    global threads
    if not ip:
        ip = "127.0.0.1"
    if not port:
        port = 11111
    with open('users.pkl', 'rb') as file:
        users = pickle.load(file)
    with open('messages.pkl','rb') as file:
        diction.socksender = pickle.load(file)
    server = socket.socket()
    server.bind((ip,port))
    server.listen(100)
    sendThread = threading.Thread(target=mgsDispatcher)
    sendThread.start()
    threads.append(sendThread)
    count = 0
    while not stop:
        count+=1
        cli = server.accept()
        t = threading.Thread(target=handl_cli,args=(cli[0],cli[1]))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    with open("users.pkl","wb") as fil:
        pickle.dump(users,fil)
    with open("messages.pkl","wb") as fil:
        pickle.dump(diction.socksender,fil)


    for t in threads:
        t.join()



if __name__ == "__main__":
    main('127.0.0.1',11111)