__author__ = "F-162A7V"

import socket, struct, PyQt5, sys, traceback, threading, pickle
import senderobject

users = {}
diction = senderobject.Sender()
stop = False


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
    try:
        code = fields[0]
        msg = ''
        if fields[0] == 'SIGN':
            if fields[1] not in users:
                users[fields[1]] = fields[2]
                diction.socksender[fields[1]] = []
                with open("users.pkl", "wb") as fil:
                    pickle.dump(users, fil)
                msg = 'SIGR|``|T'
            else:
                msg = 'EROR|``|004'
        if fields[0] == "LOGN":
            if fields[1] in users:
                if users[fields[1]] == fields[2]:

                    msg = "LOGR"
                else:
                    msg = "EROR|``|002"
            else:
                msg = "EROR|``|002"
        if fields[0] == "FGTP":
            pass
        if fields[0] == "MESG":
            keys = diction.socksender.keys()
            print(diction.socksender)
            print(fields[2])
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
    threads = []
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