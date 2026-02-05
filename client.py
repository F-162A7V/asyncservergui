__author__ = "F-162A7V"

import socket, struct, PyQt5, random


def craft_msg(inpt):


def main(ip,port,name):
    if not name:
        name = str(random.randint(0,10000000))
    if not ip:
        ip = "127.0.0.1"
    if not port:
        port = 11111
    client = socket.socket()
    try:
        client.connect((ip,port))
    except:
        print(f"unable to connect to {ip},{port}")