__author__ = "F-162A7V"

import socket, struct, PyQt5, random, sys, threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from archive.ex27.server2_7 import handle_client

stop = False
name = ""
ip = ""
port = ""


def craft_msg(inpt):
    pass


def windowwidgs(winob,w):
    b1 = QLineEdit(w)
    b2 = QLineEdit(w)
    b1.move(250,250)
    b2.move(250,280)
    b1.setFont(QFont("Arial",20))
    b2.setFont(QFont("Arial",20))
    fl = QFormLayout(w)
    fl.addRow(b1)
    fl.addRow(b2)
    b1.textChanged.connect(c1)
    b2.textChanged.connect(c2)

def window():
    winob = QApplication(sys.argv)
    w = QWidget()
    w.setGeometry(0,0,500,500)
    windowwidgs(winob,w)
    w.setWindowTitle("Client window")
    w.show()
    sys.exit(winob.exec_())

def c1(text):
    global ip
    print(text)
    ip = text

def c2(text):
    global port
    print(text)
    port = text


def sendfunc(sock,notuple):
    global stop
    while not stop:
        pass

def recvfunc(sock):
    global stop
    while not stop:
        pass

def main(ip,port):
    global name
    if not name:
        name = str(random.randint(0,10000))
    if not ip:
        ip = "127.0.0.1"
    if not port:
        port = 11111
    threads = []
    windowthread = threading.Thread(target=window)
    threads.append(windowthread)
    windowthread.start()
    client = socket.socket()
    try:
        client.connect((ip,port))
        handle_server(client)
    except TimeoutError:
        print(f"unable to connect to {ip}  at  {port}")



if __name__ == "main":
    if not sys.argv:
        main("127.0.0.1",11111)
    else:
        main(sys.argv[1],sys.argv[2])