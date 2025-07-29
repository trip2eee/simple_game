from game_object import GameObject
import math
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

        if x > 0:
            # find ground y
            ground_y = 0
            for i in range(Config.SCREEN_HEIGHT):
                if map[x,i,2] == 0:
                    ground_y = i
                    break

            # v^2 = vx^2 + vy^2
            if y < ground_y:
                self.y += self.dy * dt
            
            elif y >= ground_y:
                
                self.y -= self.dy * dt
                self.x += self.dx * dt

            self.rect.left = int(self.x)
            self.rect.bottom = int(self.y)
        else:
            valid = False