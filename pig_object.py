from game_object import GameObject
import math
import numpy as np
from config import Config

class PigObject(GameObject):
    images = None
    def __init__(self):
        super().__init__()

        if PigObject.images is None:
            image0 = self.load_image('pig0.png')
            image1 = self.load_image('pig1.png')
            PigObject.images = [
                image0,
                image1
            ]
        
        self.images = PigObject.images
        self.image = self.images[0]
        self.rect = self.images[0].get_rect()

        self.x = 1200
        self.y = 100

        # self.rect.topleft = 1200, 100
        
        self.idx_img = 0
        self.dx = -100.0
        self.dy = 100.0

    def update(self, dt):
        self.acc_time += dt
    
        num_images = len(self.images)
        self.idx_img = int(self.acc_time / 0.25) % num_images
        
        self.image = self.images[self.idx_img]

    def move(self, dt, map):
        x = int(self.rect.left + self.rect.width*0.5 + 0.5)
        y = int(self.rect.bottom)

        if 0 <= x < Config.SCREEN_WIDTH:
            # find ground y
            ground_y = y
            
            while ground_y < Config.SCREEN_HEIGHT and map[x, ground_y, 2] == Config.color_sky[2]:
                ground_y += 1

            # if the pig is over the ground
            if y < ground_y:
                self.y += self.dy * dt
            
            # if the pig is on / under the ground
            elif y >= ground_y:
                
                if x > 0:
                    # find the next y coordinate
                    next_ground_y = ground_y - 20
                    while next_ground_y < Config.SCREEN_HEIGHT and map[x-1, next_ground_y, 2] == Config.color_sky[2]:
                        next_ground_y += 1

                    dx = 1
                    dy = next_ground_y - ground_y
                    slope_angle = np.arctan2(dy, dx)

                    if slope_angle > -80 * np.pi / 180:
                        self.x += self.dx * np.cos(slope_angle) * dt
                        self.y += self.dy * np.sin(slope_angle) * dt

                else:
                    self.x += self.dx * dt

            self.rect.left = int(self.x)
            self.rect.bottom = int(self.y)
        else:
            valid = False