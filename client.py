__author__ = "F-162A7V"

import socket, struct, tkinter, random, sys, threading
import winclass


stop = False
name = ""
ip = ""
port = ""


def craft_msg(inpt):
    pass

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

def handle_server(cli):
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



if __name__ == "__main__":
    if len(sys.argv) < 3:
        main("127.0.0.1",11111)
    else:
        main(sys.argv[1],sys.argv[2])