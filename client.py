__author__ = "F-162A7V"


import socket, struct, sys, threading
import traceback
import winclass
from asyncservergui.winclass import customEntry


current_window = ""
stop = False
username = ""
threads = []


def makeSendableMSG(msg):
    length = struct.pack("I",len(msg))
    return length + msg.encode()

def recieveData(sock):
    resp = sock.recv(4)
    recvlen = struct.unpack("I",resp)
    resp = sock.recv(recvlen)
    return resp, resp.split(b'|``|')


def Pick(sock):
    global current_window
    win = winclass.Window("LOGIN", "200x400")
    current_window = win
    sign = winclass.customButton(win, 25, "LOGIN", command=lambda: signWin("", sock, 0, win), offset=(0, 20))
    log = winclass.customButton(win, 25, "SIGNUP", command=lambda: logWin("", sock, 1, win), offset=(0, 30))
    forgt = winclass.customButton(win, 25, "FORGOT PASS", command=lambda: forgotWin("", sock, 2, win), offset=(0, 40))
    win.root.mainloop()




def logWin(sock, parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    win = winclass.Window("LOGIN","200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter User:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: loginFunc(sock, namefield, passfield, win),
                                 offset=(0, 40))
    win.root.mainloop()

def signWin(sock, parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    win = winclass.Window("SIGNUP", "200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter Email:")
    emfield = winclass.customEntry(win, 25, 25, lbl="Enter Username:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: signFunc(sock, namefield, passfield,
                                                                             emfield, win),offset=(0, 40))
    win.root.mainloop()

def forgotWin(sock, parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    win = winclass.Window("FORGOT PASS", "200x300")
    current_window = win
    emfield = winclass.customEntry(win, 25, 25, lbl="Enter Email:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: forgotFunc(sock, emfield, win), offset=(0, 40))
    win.root.mainloop()




def loginFunc(sock, namefield, passfield, parent=0):
    data = f"LOGN|``|{namefield.text_var.get()}|``|{passfield.text_var.get()}"
    sock.send(makeSendableMSG(data))
    resp = recieveData(sock)
    fields = resp.split(b'|``|')
    if fields[0] == b"LOGR":
        sendWin("", sock)
    elif fields[0] == b'EROR':
        pass
    if parent:
        parent.root.destroy()

def signFunc(sock, namefield, passfield, email, parent=0):
    data = f"LOGN|``|{email}|``|{namefield.text_var.get()}|``|{passfield.text_var.get()}"
    sock.send(makeSendableMSG(data))
    resp = recieveData(sock)
    fields = resp.split(b'|``|')
    if fields[0] == b"SIGR":
        sendWin("", sock)
    elif fields[0] == b'EROR':
        pass
    if parent:
        parent.root.destroy()

def forgotFunc(sock, email, parent=0):
    data = f"FGTP|``|{email.text_var.get()}"
    sock.send(makeSendableMSG(data))
    resp = recieveData(sock)
    fields = resp.split(b'|``|')
    if fields[0] == b"FGPR":
        forgotwinP2(sock)
    return

def forgotwinP2(sock):
    win = winclass.Window("ENTER CODE", "200x300")
    codefield = winclass.customEntry(win, 25, 25, (0, 25), lbl="ENTER EMAIL CODE:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: forgotfuncP2(sock,codefield,win),offset=(0, 40))
    win.root.mainloop()

def forgotfuncP2(sock,codefield,parent=0):
    if parent:
        parent.root.destroy()
    data = f'FPCD|``|{codefield.text_var.get()}'
    sock.send(makeSendableMSG(data))
    resp = recieveData(sock)
    fields = resp.split(b'|``|')
    if fields[0] == b"FPCR":
        forgotwinP2(sock)

def forgotwinP3(sock):
    win = winclass.Window("ENTER NEW PASSWORD", "200x300")
    newpassfield = winclass.customEntry(win, 25, 25, (0, 25),shw="*", lbl="ENTER NEW PASSWORD:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: forgotfuncP3(sock,newpassfield,win),offset=(0, 40))
    win.root.mainloop()

def forgotfuncP3(sock,newpassfield,parent=0):
    if parent:
        parent.root.destroy()
    data = f'NEWP|``|{newpassfield.text_var.get()}'
    sock.send(makeSendableMSG(data))
    resp = recieveData(sock)
    fields = resp.split(b'|``|')
    if fields[0] == b"NEWR":
        print("Password changed successfully")



def sendWin(label, sock, parent=0):
    global current_window
    global threads
    reciever = threading.Thread(target=recvfunc,args=(sock,""))
    reciever.start()
    threads.append(reciever)
    if parent:
        parent.root.destroy()
    win = winclass.Window("HOME", "200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter message contents...:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), lbl="Enter target user:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: sendMsg(sock,passfield,namefield),offset=(0, 40))
    win.root.mainloop()


def sendMsg(sock,dest,msg):
    global username
    msg = f'MESG|``|{username}|``|{dest.text_var.get()}|``|{msg.text_var.get()}'
    length = struct.pack("I",len(msg))
    sock.send(length + msg.encode())


def recvfunc(sock,notuple):
    global stop
    while not stop:
        data = sock.recv(4)
        if data == b'':
            stop = True
            break
        length = struct.unpack("I", data)[0]
        data = sock.recv(length)
        fields = data.split(b'|``|')
        if fields[0] == b'MESS':
            fromuser = fields[1].decode()
            content = fields[2].decode()
            print(f"--------------------------\nNEW MESSAGE FROM: {fromuser}\n{content}\n")


def main(ip,port):
    global threads
    sock = socket.socket()
    sock.connect((ip,port))
    Pick(sock)




if __name__ == "__main__":
    if len(sys.argv) < 3:
        main("127.0.0.1",11111)
    else:
        main(sys.argv[1],sys.argv[2])