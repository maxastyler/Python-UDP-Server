from Server import Server
from queue import Queue
from time import time
from helpers import *

UPS=60.
UPDATE_TIME=1/UPS

class Game:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0
        self.o_queue=Queue()
        self.i_queue=Queue()
        self.server=Server(self.o_queue, self.i_queue)
        self.server.setup_socket()
        self.server.setDaemon(True)
        self.update_timer=time()

    def run(self):
        self.server.start()
        running=True
        while running:
            while not self.i_queue.empty():
                item=self.i_queue.get()
                if item[0]=='input':
                    if item[1]&1<<0: self.pos_y+=3
                    if item[1]&1<<1: self.pos_y-=3
                    if item[1]&1<<2: self.pos_x-=3
                    if item[1]&1<<3: self.pos_x+=3
                self.i_queue.task_done()
            if time()-self.update_timer>0.2:
                self.o_queue.put(("position", int.to_bytes(abs(self.pos_x), 4, BYTE_ORDER)+int.to_bytes(abs(self.pos_y), 4, BYTE_ORDER)))
                self.update_timer=time()

if __name__=='__main__':
    game=Game()
    game.run()
