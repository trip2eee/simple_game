from game_object import GameObject
from config import Config
import numpy as np
import pygame

class MissleObject(GameObject):
    image = None
    last_fire_time = 0

    def __init__(self):
        super().__init__()

        if MissleObject.image is None:
            MissleObject.image = self.load_image('missle.png')
        self.image = MissleObject.image
        self.rect = self.image.get_rect()

        self.rect.topleft = 1200, 100
        
        self.x = 0
        self.y = 0

        self.vx = 100.0
        self.vy = 0
        self.ax = 9.8

        self.valid = True

    def update(self, dt):
        self.acc_time += dt
    
    def move(self, dt, ground):
        
        self.vy += self.ax*dt
        self.x += self.vx * dt
        self.y += self.vy * dt


        angle = np.arctan2(-self.vy, self.vx) * 180 / np.pi
        self.image = pygame.transform.rotate(MissleObject.image, angle)

        self.rect.left = int(self.x - self.rect.width*0.5)
        self.rect.top = int(self.y - self.rect.height*0.5)
        
        if self.x >= Config.SCREEN_WIDTH or self.y >= Config.SCREEN_HEIGHT:
            self.valid = False
        else:
            x = int(self.x + 0.5)
            y = int(self.y + 0.5)
            
            
            if 0 <= x < Config.SCREEN_WIDTH and 0 <= y < Config.SCREEN_HEIGHT and ground[x,y,2] == Config.color_ground[2]:
                
                r = int(self.rect.width*0.5)
                x0 = max(0, x-r)
                x1 = min(Config.SCREEN_WIDTH-1, x+r)
                y0 = max(0, y-r)
                y1 = min(Config.SCREEN_HEIGHT-1, y+r)
                
                ground[x0:x1, y0:y1, :] = Config.color_sky

                self.valid = False

    def explode(self, map, sprites_enemies): 
        
        x_center = self.rect.left + int(self.rect.width*0.5 + 0.5)
        y_center = self.rect.top + int(self.rect.height*0.5 + 0.5)
        r_thres = 100
        r2_thres = r_thres**2

        y0 = max(0, y_center - r_thres)
        y1 = min(Config.SCREEN_HEIGHT-2, y_center + r_thres)
        x0 = max(0, x_center - r_thres)
        x1 = min(Config.SCREEN_WIDTH-2, x_center + r_thres)
        if x1 > x0 and y1 > y0:
            # dig the ground
            xs = np.linspace(x0, x1+1, x1-x0+2, dtype=np.int32)
            ys = np.linspace(y0, y1+1, y1-y0+2, dtype=np.int32)
            xv, yv = np.meshgrid(xs, ys, indexing='xy')
            
            dx = xv - x_center
            dy = yv - y_center
            r2 = dx**2 + dy**2
            idx = np.where(r2 < r2_thres)

            x_dig = xv[idx]
            y_dig = yv[idx]
            map[x_dig, y_dig] = Config.color_sky

        # kill enemies
        list_enemies = sprites_enemies.sprites()
        for enemy in list_enemies:
            x_enemy = enemy.rect.left + (enemy.rect.width * 0.5)
            y_enemy = enemy.rect.top + (enemy.rect.height * 0.5)
            dx = x_center - x_enemy
            dy = y_center - y_enemy
            r2 = dx**2 + dy**2

            if r2 < r2_thres:
                enemy.valid = False
                sprites_enemies.remove(enemy)

           