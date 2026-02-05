__author__ = "F-162A7V"

import socket, struct, PyQt5



def handl_cli():


def main(ip,port):
    if not ip and not port:
        ip, port = "127.0.0.1", 11111

    server = socket.socket()
    server.bind(())











if __name__ == "main":
    main()