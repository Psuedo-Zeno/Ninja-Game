import pygame as pg
import sys

from settings import *
from level import Level

class Main:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Physics Game")
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.clock = pg.time.Clock()
        self.level = Level(level_map, self.screen)

    def run(self):
        while True: 
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit()
                    sys.exit()
            self.screen.fill('orange')
            self.level.run()
            pg.display.flip()

            pg.display.update()
            self.clock.tick(60) 
        
if(__name__ == "__main__"):
    app = Main()
    app.run()