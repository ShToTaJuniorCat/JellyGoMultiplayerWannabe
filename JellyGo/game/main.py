import pygame
from jelly_tower import JellyTower
from player import Player
from constants import *


pygame.init()
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("Jelly Go")

# Create sprite groups and enable the layered flag
tower_group = pygame.sprite.LayeredUpdates()

red_player = Player((255, 0, 0), "RED-PLAYER")
tower = JellyTower(100, 100, 1, red_player, 0.0, 50, 1, 50, 2, "barracks")
tower.layer = 1

tower_group.add(tower)

tower_group.draw(screen)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            print("Hello")

    tower.tick(screen)
    tower.dirty = True
    tower_group.clear(screen, screen)
    tower_group.draw(screen)
    pygame.display.update()
