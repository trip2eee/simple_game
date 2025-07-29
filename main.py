import pygame
from game_object import GameObject
from pig_object import PigObject
from bullet_object import BulletObject
from missle_object import MissleObject
from config import Config

import numpy as np

# https://www.pygame.org/docs/
# game setup
pygame.init()

screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

dt = 0
acc_time = 0
spawn_time = 0

player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

sprites_enemies = pygame.sprite.RenderPlain()
sprites_bullets = pygame.sprite.RenderPlain()

ground_y0 = 720//2

fire_angle = 0
gun_height = ground_y0 - 10

map = np.zeros([Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, 3], dtype=np.uint8)
map[:,:ground_y0,:] = Config.color_sky
map[:,ground_y0:,:] = Config.color_ground

GameObject.set_map(map)

while running:
    # poll for events
    # pygame.QUIT event means that user clicked X to close your window.
    for event in pygame.event.get():
        if pygame.QUIT == event.type:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("skyblue")

    # RENDER YOUR GAME HERE

    surface_map = pygame.pixelcopy.make_surface(map)
    screen.blit(surface_map, (0,0))

    if acc_time > spawn_time + 1.0:
        spawn_time = acc_time
        pig = PigObject()
        sprites_enemies.add(pig)

    len_gun = 20
    gun_x = len_gun*np.cos(fire_angle * np.pi / 180)
    gun_y = gun_height - len_gun*np.sin(fire_angle * np.pi / 180)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        fire_angle += 0.5
        if fire_angle >= 90:
            fire_angle = 90
    if keys[pygame.K_DOWN]:
        fire_angle -= 0.5
        if fire_angle <= -90:
            fire_angle = -90
    if keys[pygame.K_SPACE]:
        #bullet = BulletObject()
        if acc_time > MissleObject.last_fire_time + 1.0:
            MissleObject.last_fire_time = acc_time
            bullet = MissleObject()
            bullet.x = gun_x
            bullet.y = gun_y
            v = 150
            bullet.vx = v*np.cos(fire_angle * np.pi / 180)
            bullet.vy = -v*np.sin(fire_angle * np.pi / 180)
            
            sprites_bullets.add(bullet)

    pygame.draw.line(screen, color=(255,0,0), start_pos=(0, gun_height), end_pos=(gun_x, gun_y), width=2)
    
    list_bullet = sprites_bullets.sprites()
    for bullet in list_bullet:
        bullet.update(dt)
        bullet.move(dt, map)

    list_bullet = sprites_bullets.sprites()
    list_enemies = sprites_enemies.sprites()
    for enemy in list_enemies:
        enemy.update(dt)
        enemy.move(dt, map)

        if enemy.valid:
            for bullet in list_bullet:
                if bullet.valid:
                    collision = enemy.test_collision(bullet)

                    if collision:
                        if isinstance(bullet, MissleObject):
                            bullet.explode(map, sprites_enemies)

                        enemy.valid = False
                        bullet.valid = False
                        sprites_bullets.remove(bullet)
                        sprites_enemies.remove(enemy)
                else:
                    if isinstance(bullet, MissleObject):
                        bullet.explode(map, sprites_enemies)
                    sprites_bullets.remove(bullet)
        else:
            sprites_enemies.remove(enemy)

    # update ground lut
    GameObject.set_map(map)
            
    sprites_enemies.draw(screen)
    sprites_bullets.draw(screen)

    # flip() the display to put your work on screen.
    pygame.display.flip()

    # limits FPS to 60.
    # dt is delta time in seconds since last frame. used for 
    # framerate-independent physics.
    dt = clock.tick(60) / 1000
    acc_time += dt

pygame.quit()

