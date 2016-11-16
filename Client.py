import socket
from helpers import *
from threading import Thread
from queue import Queue
from Connection import Connection
from time import sleep, time

class Client(Thread):
    def __init__(self, incoming_queue, outgoing_queue, address="127.0.0.1", port=10000):
        super().__init__()
        self.socket_setup=False
        self.incoming_queue=incoming_queue
        self.outgoing_queue=outgoing_queue
        self.address=(address, port)
        self.connected=False
        self.connection=None
        self.alive_time=time()
        self.username=None

    def setup_socket(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)
        self.socket_setup=True

    def run(self):
        if self.socket_setup!=True:
            print("Socket not setup! Run Client.socket_setup() first")
            return
        while True:
            input_bytes=None
            while not self.incoming_queue.empty():
                input_bytes=self.incoming_queue.get()
                self.incoming_queue.task_done()
            if input_bytes is not None:
                self.connection.send_data(BYTE_COMMAND['input']+input_bytes, self.sock) 
            if not self.connected:
                self.initiate_connection(self.address)
            else:
                data=False
                try:
                    data, addr= self.sock.recvfrom(PACKET_SIZE)
                except BlockingIOError:
                    pass
                if data:
                    if data[0:8]==HEADER_NAME+self.username:
                        processed_data=self.connection.process_data(data[8:])
                        if processed_data is not None:
                            self.outgoing_queue.put(processed_data)
                        
                if time()-self.alive_time>0.6:
                    self.alive_time=time()
                    if self.connection is not None:
                        self.connection.tell_alive(self.sock)
                        if time()-self.connection.last_message_time>CONNECTION_TIME_OUT:
                            self.connection=None
                            self.connected=False

    def initiate_connection(self, address):
        time_out=False
        count=0
        while not self.connected and not time_out:
            self.sock.sendto(HEADER_NAME+BYTE_COMMAND['connect'], self.address)
            t_now=time()
            while time()-t_now<2:
                addr=None
                data=None
                try:
                    data, addr = self.sock.recvfrom(PACKET_SIZE)
                except Exception as e:
                    pass
                if addr==self.address and data[0:8]==HEADER_NAME+BYTE_COMMAND['accept_connection']:
                    self.connection=Connection(addr, data[8:PACKET_SIZE])
                    self.username=data[8:PACKET_SIZE]
                    self.connected=True
                    break
            sleep(1)
            count+=1
            if count>10:
                time_out=True
        print("CONNECTED")
                
if __name__=='__main__':
    i_queue=Queue()
    o_queue=Queue()
    client=Client(o_queue, i_queue)
    client.setup_socket()
    client.setDaemon(True)
    client.start()
    while True:
        pass
