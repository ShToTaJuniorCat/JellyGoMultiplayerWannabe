import pygame
from jelly_tower import JellyTower
from player import Player
from constants import *


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jelly Go")

# Load the background image
background_image = pygame.image.load(r"../assets/images/background.jpg")

# Scale the background image to match the size of self.image
image_width, image_height = screen.get_size()
background_image = pygame.transform.scale(background_image, (image_width, image_height))

# Blit the background image onto self.image
screen.blit(background_image, (0, 0))  # Place it in the top-left corner

# Create sprite groups and enable the layered flag
tower_group = pygame.sprite.LayeredUpdates()

red_player = Player((255, 0, 0), "RED-PLAYER")
tower1 = JellyTower(200, 300, 1, red_player, 0.0, 50, 1, 50, 10, "fort")
tower1.layer = 0

blue_player = Player((0, 0, 255), "BLUE-PLAYER")
tower2 = JellyTower(500, 300, 1, blue_player, 10.0, 10, 1, 50, 0.4, "barracks")
tower3 = JellyTower(500, 600, 1, blue_player, 10.0, 10, 1, 50, 0.4, "barracks")
tower2.layer = 0
tower3.layer = 0

tower_group.add(tower1)
tower_group.add(tower2)
tower_group.add(tower3)

tower_group.draw(screen)

selected_towers = []
run = True
clicked = False
mouse_pos = None
selection_area_start = None
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_SPACE:
                for tower in tower_group:
                    if tower.tower_type == "barracks":
                        selected_towers.append(tower)

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selection_area_start = pygame.mouse.get_pos()
             selected_towers = []

    tower_clicked = False
    mouse_pos = pygame.mouse.get_pos()
    for tower in tower_group:
        if tower.get_bounding_box().collidepoint(mouse_pos):
            tower.hovered = True
            tower_clicked = True

            if clicked:
                tower.click_position = mouse_pos

                if tower.get_tower_bounding_box().collidepoint(mouse_pos):
                    if not selected_towers:
                        print(selected_towers)
                        selected_towers.append(tower)
                    else:
                        print("Send jellies to this tower!")
                        selected_towers = []

        else:
            tower.hovered = False

        tower.tick()

    if selection_area_start:
        end_x, end_y = pygame.mouse.get_pos()
        start_x, start_y = selection_area_start

        # Calculate the square's position and dimensions
        square_x = min(start_x, end_x)
        square_y = min(start_y, end_y)
        square_width = abs(end_x - start_x)
        square_height = abs(end_y - start_y)

        # Draw the transparent square
        transparent_surface = pygame.Surface((square_width, square_height), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (255, 255, 255, 128), (0, 0, square_width, square_height), 0)
        screen.blit(transparent_surface, (square_x, square_y))

    if not tower_clicked:
        if clicked:
            if selection_area_start:
                print(f"Select area from {selection_area_start} to {pygame.mouse.get_pos()}")
                selection_area_start = None
            else:
                selected_towers = []
    else:
        selection_area_start = None

    tower_group.clear(screen, screen)
    tower_group.draw(screen)

    for tower in selected_towers:
        pygame.draw.line(surface=screen,
                         color=(255, 255, 255),
                         start_pos=mouse_pos,
                         end_pos=(tower.tower_x - (TOWERS_WIDTH / 2),
                                  tower.tower_y - ATTRIBUTES_SURFACE_HEIGHT - (TOWERS_WIDTH / 2)),
                         width=4)

    pygame.display.update()

    # Blit the background image onto self.image
    screen.blit(background_image, (0, 0))  # Place it in the top-left corner

    clicked = False
