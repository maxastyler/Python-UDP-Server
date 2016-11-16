import socket
from helpers import *
from threading import Thread
from queue import Queue
from Connection import Connection

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

class Client(Thread):
    def __init__(self, incoming_queue, outgoing_queue, address="localhost", port=10000):
        super().__init__()
        self.socket_setup=False
        self.incoming_queue=incoming_queue
        self.outgoing_queue=outgoing_queue
        self.address=(address, port)
        self.connected=False

    def setup_socket(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.socket_setup=True

    def run(self):
        if self.socket_setup!=True:
            print("Socket not setup! Run Client.socket_setup() first")
            return
        while True:
            if not self.connected:
                self.try_to_connect()
            else:
                data=False
                msg=input("MESSAGE: ")
                sock.sendto(create_packet(BYTE_COMMAND['connect']), address)
                try:
                    data, addr= sock.recvfrom(PACKET_SIZE)
                except BlockingIOError:
                    pass
                if data:
                    print(data)

    def try_to_connect(self):
        pass

if __name__=='__main__':
    i_queue=Queue()
    o_queue=Queue()
    client=Client(o_queue, i_queue)
    client.setup_socket()
    client.setDaemon(True)
    client.start()
    while True:
        pass
