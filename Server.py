import socket
from time import sleep
from queue import Queue
from threading import Thread
from helpers import *
from Connection import Connection
from sys import exit

class Server(Thread):
    def __init__(self, incoming_queue, outgoing_queue, address="", port=10000):
        super().__init__()
        self.address=address
        self.incoming_queue=incoming_queue
        self.outgoing_queue=outgoing_queue
        self.port=port
        self.socket_setup=False
        self.active_connections={} #Store with player_id:connection_data

    def setup_socket(self):
        try:
            self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except:
            exit("Couldn't create a socket")
        try:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setblocking(False)
        except:
            exit("Couldn't set socket options")
        self.server_details=(self.address, self.port)
        try:
            self.sock.bind(self.server_details)
        except:
            exit("Couldn't bind socket to server address")
        self.socket_setup=True

    def run(self):
        if self.socket_setup!=True:
            print("Socket hasn't been setup. Do that first!")
            return
        while True:
            while not self.incoming_queue.empty():
                print(self.incoming_queue.get())
                self.incoming_queue.task_done()
            data=False
            try:
                data, addr=self.sock.recvfrom(PACKET_SIZE)
            except BlockingIOError:
                pass
            if data:
                if data[0:4]==HEADER_NAME and len(data)>=4: 
                    #We have received a packet with the correct header. Time to process it.
                    data=data[4:]
                    if data == BYTE_COMMAND['connect']:
                        self.initiate_connection(addr)

    def initiate_connection(self, address):
        pass


if __name__=='__main__':
    i_queue=Queue()
    o_queue=Queue()
    server=Server(o_queue, i_queue)
    server.setup_socket()
    server.setDaemon(True)
    server.start()
    while True:
        pass
