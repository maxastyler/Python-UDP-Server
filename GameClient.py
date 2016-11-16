import pygame
from Client import Client
from queue import Queue
from time import sleep, time
from helpers import *
import sys

FPS=30.
UPDATE_TIME=1/FPS
SCREEN_SIZE=(640, 480)

def make_input_bytes(keys):
    input_mask=keys[pygame.K_UP]<<0
    input_mask|=keys[pygame.K_DOWN]<<1
    input_mask|=keys[pygame.K_LEFT]<<2
    input_mask|=keys[pygame.K_RIGHT]<<3
    if input_mask!=0:
        return int.to_bytes(input_mask, 4, BYTE_ORDER)
    else:
        return None

class GameClient:
    def __init__(self):
        self.i_queue=Queue()
        self.o_queue=Queue()
        self.client=Client(self.o_queue, self.i_queue, address=sys.argv[1])
        self.client.setup_socket()
        self.client.setDaemon(True)
        self.pos_x=0
        self.pos_y=0
        self.input_timer=time()

    def run(self):
        self.client.start()
        running=True
        print("Running main loop")

        screen=pygame.display.set_mode(SCREEN_SIZE)

        while running:
            time_start=time()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                    break
            while not self.i_queue.empty():
                item=self.i_queue.get()
                if item[0]=='position':
                    self.pos_x=item[1]
                    self.pos_y=item[2]
                self.i_queue.task_done()
            input_bytes=make_input_bytes(pygame.key.get_pressed())
            if input_bytes is not None and time()-self.input_timer>0.05:
                self.input_timer=time()
                self.o_queue.put(input_bytes)
            screen.fill((255, 255, 255))
            pygame.draw.circle(screen, (0, 0, 0), (self.pos_x, self.pos_y), 10)
            pygame.display.update()

        pygame.quit() 

if __name__=='__main__':
    pygame.init()
    game=GameClient()
    sys.exit(game.run())
