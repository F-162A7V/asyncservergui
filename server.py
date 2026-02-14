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
            try:
                diction.DelNameSocket(user)
            except:
                pass
            break
        len = struct.unpack("I",len)
        data = sock.recv(len)
        if data == b'':
            try:
                diction.DelNameSocket(user)
            except:
                pass
            break
        data = data.decode()
        fields = data.split('|')
        parse_msg(fields,sock)


def parse_msg(fields,sock):
    global users
    code = fields[0]
    msg = ''
    if fields[0] == 'SIGN':
        if fields[1] not in users:
            users[fields[1]] = fields[2]
            msg = 'SIGR|T'
        else:
            msg = 'SIGR|F'
    if fields[0] == "LOGN":
        if fields[1] in users:
            if users[fields[1]] == fields[2]:
                msg = "LOGR|T"
            else:
                msg = "EROR|002"
        else:
            msg = "LOGR|F"
    if fields[0] == "FGTP":
        pass
    if fields[0] == "MESG":
        if fields[1] in diction.sock_by_name:
            sender = ""
            for t in diction.sock_by_name:
                if diction.sock_by_name[t] == sock:
                    sender = t
            msg = f'MESS|{sender}|{fields[2]}'
        else:
            msg = "EROR|003"
    length = struct.pack("I",len(msg))
    msg = length + msg.encode()
    if msg[:4] == "MESS":
        try:
            diction.sock_by_name[fields[1]].send(msg)
        except:
            msg = "EROR|001"
            length = struct.pack("I",len(msg))
            msg = length + msg.encode()
    else:
        try:
            sock.send(msg)
        except:
            pass




def main(ip,port):
    global stop
    if not ip:
        ip = "127.0.0.1"
    if not port:
        port = 11111
    #users = pickle.load()
    server = socket.socket()
    server.bind((ip,port))
    server.listen(100)
    threads = []
    while not stop:
        cli = server.accept()
        t = threading.Thread(target=handl_cli,args=(cli[0],cli[1]))
        threads.append(t)


    for t in threads:
        t.join()



if __name__ == "__main__":
    main('127.0.0.1',11111)