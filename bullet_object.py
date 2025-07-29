from game_object import GameObject
from config import Config

class BulletObject(GameObject):
    image = None
    last_fire_time = 0

    def __init__(self):
        super().__init__()

        if BulletObject.image is None:
            BulletObject.image = self.load_image('bullet.png')
        self.image = BulletObject.image
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
    
    def move(self, dt, map):
        
        self.vy += self.ax*dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.rect.left = int(self.x - self.rect.width*0.5)
        self.rect.top = int(self.y - self.rect.height*0.5)
        
        if self.x >= Config.SCREEN_WIDTH or self.y >= Config.SCREEN_HEIGHT:
            self.valid = False
        else:
            x = int(self.x + 0.5)
            y = int(self.y + 0.5)
            
            if 0 <= x < Config.SCREEN_WIDTH and 0 <= y < Config.SCREEN_HEIGHT and map[x,y,2] == Config.color_sky[2]:
                
                r = int(self.rect.width*0.5)
                x0 = max(0, x-r)
                x1 = min(Config.SCREEN_WIDTH-1, x+r)
                y0 = max(0, y-r)
                y1 = min(Config.SCREEN_HEIGHT-1, y+r)
                
                map[x0:x1, y0:y1, :] = Config.color_sky

                self.valid = False
