__author__ = "F-162A7V"

import socket, struct, tkinter, random, sys, threading
import winclass


stop = False
mail = ""
password = ""

def craft_msg(inpt):
    pass

def logwin():
    win = winclass.Window("LOGIN","200x300")
    namefield = winclass.customEntry(win, 25, 25, lbl="Enter Name:")
    passfield = winclass.customEntry(win, 25, 25, (0, 25), "*", lbl="Enter Password:")
    send = winclass.customButton(win,25,"submit",command=logret(namefield,passfield,win),offset=(0,40))
    win.root.mainloop()

def logret(namefield,passfield,prntwin):
    returntup = (namefield.text_var.get(), passfield.text_var.get())
    prntwin.root.destroy()
    print(returntup)
    return returntup

def c2():
    global mail
    global password
    print(mail)
    print(password)

def sendfunc(sock,notuple):
    global stop
    while not stop:
        pass

def recvfunc(sock):
    global stop
    while not stop:
        pass

def handle_server(cli):
    pass

def main(ip,port):
    sock = socket.socket()
    sock.connect((ip,port))
    threads = []
    logwin()



if __name__ == "__main__":
    if len(sys.argv) < 3:
        main("127.0.0.1",11111)
    else:
        main(sys.argv[1],sys.argv[2])