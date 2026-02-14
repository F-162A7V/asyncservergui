import socket, struct


class Sender:
    def __init__(self):
        self.sock_by_name = {}
        self.socksender = {}

    def AddNameSocket(self,socket,name):
        self.sock_by_name[name] = socket

    def DelNameSocket(self,name):
        self.sock_by_name.pop(name,None)

    def AddMsg(self,name,msg):
        self.socksender[self.sock_by_name[name]] = msg