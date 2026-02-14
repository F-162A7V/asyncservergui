__author__ = "F-162A7V"

import socket, struct, sys, threading
import winclass

current_window = ""
stop = False
mail = ""
password = ""

def craft_msg(inpt):
    pass


def Pick(sock):
    global current_window
    win = winclass.Window("LOGIN", "200x200")
    current_window = win
    sign = winclass.customButton(win, 25, "LOGIN", command=lambda: logwin("",sock,win),offset=(0, 20))
    log = winclass.customButton(win, 25, "SIGNUP", command=lambda: signwin("",sock,win),offset=(0, 30))
    win.root.mainloop()

def logwin(label,sock,parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    win = winclass.Window("LOGIN","200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter Name:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win,25,"Submit",command=lambda:logret(namefield,passfield,win,sock),offset=(0,40))
    win.root.mainloop()

def signwin(label,sock,parent=0):
    global current_window
    if parent:
        parent.root.destroy()
    win = winclass.Window("SIGNUP", "200x300")
    current_window = win
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter Name:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win, 25, "Submit", command=lambda: signret(namefield, passfield, win, sock),offset=(0, 40))
    win.root.mainloop()

def logret(namefield,passfield,prntwin,skt):
    global stop
    data = f"LOGN|{namefield.text_var.get()}|{passfield.text_var.get()}"
    lngth = struct.pack("I",len(data))
    data = lngth + data.encode()
    try:
        skt.send(data)
    except:
        stop = True
    prntwin.root.destroy()
    return

def signret(namefield,passfield,prntwin,skt):
    global stop
    data = f"SIGN|{namefield.text_var.get()}|{passfield.text_var.get()}"
    lngth = struct.pack("I", len(data))
    data = lngth + data.encode()
    try:
        skt.send(data)
    except:
        stop = True
    prntwin.root.destroy()
    resp = 
    return


def sendfunc(sock,notuple):
    global stop
    while not stop:
        pass



def recvfunc(sock):
    global stop
    while not stop:
        data = sock.recv(4)
        if data == b'':
            stop = True
            break
        length = struct.unpack("I", data)
        data = sock.recv(length)



def handle_server(cli):
    pass

def main(ip,port):
    sock = socket.socket()
    sock.connect((ip,port))
    threads = []
    Pick(sock)



if __name__ == "__main__":
    if len(sys.argv) < 3:
        main("127.0.0.1",11111)
    else:
        main(sys.argv[1],sys.argv[2])