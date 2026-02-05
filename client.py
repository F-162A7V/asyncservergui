__author__ = "F-162A7V"

import socket, struct, PyQt5, random, sys, threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from archive.ex27.server2_7 import handle_client


def craft_msg(inpt):
    pass

def Window():
    winob = QApplication(sys.argv)
    w = QWidget()
    b = QLineEdit()
    w.setGeometry(0,0,500,500)
    w.setWindowTitle("Client window")
    b.move(250,250)
    w.show()
    sys.exit(winob.exec_())

def main(ip,port,name):
    threads = []
    windowthread = threading.Thread(target=Window(),args=())
    threads.append(windowthread)
    windowthread.start()    
    client = socket.socket()
    try:
        client.connect((ip,port))
    except:
        print(f"unable to connect to {ip},{port}")