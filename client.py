__author__ = "F-162A7V"

import socket, struct, sys, threading
import traceback

import winclass

current_window = ""
stop = False
username = ""
threads = []

def craft_msg(inpt):
    pass


def Pick(sock):
    global current_window
    win = winclass.Window("LOGIN", "200x200")
    current_window = win
    sign = winclass.customButton(win, 25, "LOGIN", command=lambda: logwin("",sock,0,win),offset=(0, 20))
    log = winclass.customButton(win, 25, "SIGNUP", command=lambda: logwin("",sock,1,win),offset=(0, 30))
    win.root.mainloop()

def logwin(label, sock, typef, parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    if typef:
        win = winclass.Window("SIGNUP","200x300")
    else:
        win = winclass.Window("LOGIN","200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter Name:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: logret(namefield, passfield, win, sock, typef), offset=(0, 40))
    win.root.mainloop()

def logret(namefield, passfield, prntwin, skt, typef):
    global stop, username
    username = namefield.text_var.get()
    if typef:
        data = f"SIGN|``|{namefield.text_var.get()}|``|{passfield.text_var.get()}"
    else:
        data = f"LOGN|``|{namefield.text_var.get()}|``|{passfield.text_var.get()}"
    lngth = struct.pack("I",len(data))
    data = lngth + data.encode()
    skt.send(data)
    prntwin.root.destroy()
    resp = skt.recv(4)
    length = struct.unpack("I",resp)[0]
    resp = skt.recv(length)
    fields = resp.split(b'|``|')
    if typef:
        if fields[0] == b"SIGR":
            sendWin("", skt)
    else:
        if fields[0] == b"LOGR":
            sendWin("", skt)
    return


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