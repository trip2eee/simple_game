import os
import pygame as pg
import math
from config import Config

class GameObject(pg.sprite.Sprite):
    ground = None
    ground_y_lut = None

    @staticmethod
    def set_map(ground):
        GameObject.ground = ground
        width = ground.shape[0]
        height = ground.shape[1]

        ground_y_lut = [0] * width
        for x in range(width):
            for y in range(height):
                if ground[x, y, 2] == Config.color_ground[2]:
                    ground_y_lut[x] = y
                    break

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = None
        self.acc_time = 0
        self.valid = True
    
    def load_image(self, file_name, colorkey=None, scale=1):
        full_name = os.path.join('./data/image', file_name)
        image = pg.image.load(full_name)

        size = image.get_size()
        size = (size[0] * scale, size[1]*scale)
        image = pg.transform.scale(image, size)

        # image = image.convert()
        image = image.convert_alpha()
        if colorkey is not None:
            if -1 == colorkey:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image
    
    def update(self, dt):
        pass

    def move(self, dt, ground_xy):
        pass

    def test_collision(self, target):
        tx = target.rect.left + (target.rect.width * 0.5)
        ty = target.rect.top + (target.rect.height * 0.5)
        tr2 = (target.rect.width*0.5)**2 + (target.rect.height*0.5)**2
        
        x = self.rect.left + (self.rect.width * 0.5)
        y = self.rect.top + (self.rect.height * 0.5)
        r2 = (self.rect.width*0.5)**2 + (self.rect.height*0.5)**2

        max_r2 = max(r2, tr2)

        dx = x - tx
        dy = y - ty
        if (dx**2 + dy**2) < max_r2:
            return True
        else:
            return False

