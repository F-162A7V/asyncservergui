__author__ = "F-162A7V"

import socket, struct, PyQt5, sys, traceback

from PyQt5.QtWidgets import QApplication


def window():
    app = QApplication("test1")

def handl_cli():
    pass

def main(ip,port):
    if not ip:
        ip = "127.0.0.1"
    if not port:
        port = 11111

    server = socket.socket()
    server.bind(())











if __name__ == "main":
    main()