import pygame
from jelly_tower import JellyTower
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jelly Go")

# Load the background image
background_image = pygame.image.load(r"../assets/images/background.jpg")

# Scale the background image to match the size of self.image
image_width, image_height = screen.get_size()
background_image = pygame.transform.scale(background_image, (image_width, image_height))

# Blit the background image onto self.image
screen.blit(background_image, (0, 0))  # Place it at the top-left corner

# Create sprite groups and enable the layered flag
tower_group = pygame.sprite.LayeredUpdates()

red_player = Player((255, 0, 0), "RED-PLAYER")
tower1 = JellyTower(100, 100, 1, red_player, 0.0, 50, 1, 50, 10, "barracks")
tower1.layer = 1

blue_player = Player((0, 0, 255), "BLUE-PLAYER")
tower2 = JellyTower(200, 300, 1, blue_player, 10.0, 10, 1, 50, 0.4, "barracks")
tower2.layer = 0

# tower_group.add(tower1)
tower_group.add(tower2)

tower_group.draw(screen)

run = True
clicked = False
mouse_pos = None
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True

    mouse_pos = pygame.mouse.get_pos()
    for tower in tower_group:
        if tower.get_bounding_box().collidepoint((mouse_pos)):
            tower.hovered = True

            if clicked:
                tower.click_position = mouse_pos

                if tower.get_tower_bounding_box().collidepoint((mouse_pos)):
                    print("SELECTED")
        else:
            tower.hovered = False

        tower.tick()

    # tower2.dirty = True
    tower_group.clear(screen, screen)
    tower_group.draw(screen)

    pygame.display.update()

    # Blit the background image onto self.image
    screen.blit(background_image, (0, 0))  # Place it at the top-left corner

    clicked = False