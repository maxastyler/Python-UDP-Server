import socket
from time import sleep, time
from queue import Queue
from threading import Thread
from helpers import *
from Connection import Connection
from sys import exit
from random import randint

class Server(Thread):
    def __init__(self, incoming_queue, outgoing_queue, address="", port=10000):
        super().__init__()
        self.address=address
        self.incoming_queue=incoming_queue
        self.outgoing_queue=outgoing_queue
        self.port=port
        self.socket_setup=False
        self.active_connections={} #Store with player_id:connection_data
        self.dead_connections={}
        self.alive_time=time()

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
                    if data[0:4] in self.active_connections:
                        self.active_connections[data[0:4]].process_data(data[4:]) 
                    if data == BYTE_COMMAND['connect']:
                        self.initiate_connection(addr)
            if time()-self.alive_time>1:
                self.alive_time=time()
                connections_to_drop=[]
                for key in self.active_connections:
                    self.active_connections[key].tell_alive(self.sock)
                    if time()-self.active_connections[key].last_message_time>CONNECTION_TIME_OUT:
                        connections_to_drop.append(key)
                for key in connections_to_drop:
                    self.dead_connections[key]=self.active_connections.pop(key)

    def initiate_connection(self, address):
        while True:
            username=fnv1a(int.to_bytes(randint(0, INT32_MAX), 4, BYTE_ORDER))
            if not username in self.active_connections:
                break
        self.sock.sendto(HEADER_NAME+BYTE_COMMAND['accept_connection']+username, address)
        self.active_connections[username]=Connection(address, username)
        print("CONNECTED to ", username)


if __name__=='__main__':
    i_queue=Queue()
    o_queue=Queue()
    server=Server(o_queue, i_queue)
    server.setup_socket()
    server.setDaemon(True)
    server.start()
    while True:
        pass
