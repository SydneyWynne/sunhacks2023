import pygame, sys
from settings import *
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(levelOne, screen, '../sunhacks2023/graphics/level1BackgroundFixed.png', (12,-5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((212,180,140))
    if level.run() == 1:
        print('good work you cheeky wanker')

    pygame.display.update()
    clock.tick(60)
