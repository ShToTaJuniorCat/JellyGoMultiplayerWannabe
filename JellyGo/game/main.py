import pygame
from jelly_tower import JellyTower
from player import Player
from constants import *


def send_jellies(sending_towers, receiving_tower, amount):
    print(f"Send {amount} from {len(sending_towers)} towers to {receiving_tower.owner.identifier}")


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

# Players
neutral_player = Player(GRAY, "NEUTRAL-PLAYER")
red_player = Player(RED, "RED-PLAYER")
current_user = Player(BLUE, "BLUE-PLAYER")

# Neutral player's towers
neutral_player_towers = [
    JellyTower(tower_x=265, tower_y=220, level=1, owner=neutral_player, current_jellies=20.0,
               max_jellies=10, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="barracks", is_current_player=False),  # top first
    JellyTower(tower_x=250, tower_y=950, level=1, owner=neutral_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="fort", is_current_player=False),  # bottom first
    JellyTower(tower_x=1020, tower_y=220, level=1, owner=neutral_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="house", is_current_player=False)  # top third
]

# Red player's towers
red_player_towers = [
    JellyTower(tower_x=1370, tower_y=220, level=1, owner=red_player, current_jellies=20.0,
               max_jellies=10, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="barracks", is_current_player=False),  # top fourth
    JellyTower(tower_x=1350, tower_y=600, level=1, owner=red_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="barracks", is_current_player=False),  # middle fourth
    JellyTower(tower_x=1350, tower_y=950, level=1, owner=red_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="house", is_current_player=False),  # bottom fourth
    JellyTower(tower_x=1015, tower_y=950, level=1, owner=red_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="lab", is_current_player=False),  # bottom third
    JellyTower(tower_x=1015, tower_y=600, level=1, owner=red_player, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="fort", is_current_player=False),  # middle third
]

# Blue player's towers
blue_player_towers = [
    JellyTower(tower_x=560, tower_y=220, level=1, owner=current_user, current_jellies=20.0,
               max_jellies=10, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="fort", is_current_player=True),  # top second
    JellyTower(tower_x=560, tower_y=600, level=1, owner=current_user, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="barracks", is_current_player=True),  # middle second
    JellyTower(tower_x=560, tower_y=950, level=1, owner=current_user, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="lab", is_current_player=True),  # bottom second
    JellyTower(tower_x=265, tower_y=600, level=1, owner=current_user, current_jellies=50.0,
               max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
               tower_type="barracks", is_current_player=True)  # middle first
]

towers_by_player = [neutral_player_towers, red_player_towers, blue_player_towers]

for player in towers_by_player:
    for tower in player:
        tower_group.add(tower)

tower_group.draw(screen)

selected_towers = []
run = True
clicked = None
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
                    if tower.tower_type == "barracks" and tower.owner is current_user:
                        selected_towers.append(tower)

        if event.type == pygame.MOUSEBUTTONUP:
            clicked = (int(event.button / 2) / 2) + 0.5
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Only select when clicking with left mouse button
                for tower in tower_group:
                    if tower.get_bounding_box().collidepoint(pygame.mouse.get_pos()):
                        break
                else:
                    selection_area_start = pygame.mouse.get_pos()
                    selected_towers = []

    tower_clicked = False
    mouse_pos = pygame.mouse.get_pos()
    for tower in tower_group:
        tower.tick()

        if selection_area_start:
            continue

        if tower.get_bounding_box().collidepoint(mouse_pos):
            tower.hovered = True

            if clicked:
                tower_clicked = True
                tower.click_position = mouse_pos

                if tower.get_tower_bounding_box().collidepoint(mouse_pos):
                    if not selected_towers and tower.owner is current_user:
                        selected_towers.append(tower)
                    elif selected_towers:
                        send_jellies(selected_towers, tower, clicked)
                        selected_towers = []

        else:
            tower.hovered = False

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
        if clicked == 0.5:
            if selection_area_start:
                selection_area_end = pygame.mouse.get_pos()

                for tower in tower_group:
                    tower_x, tower_y, tower_width, tower_height = tower.get_tower_bounding_box()
                    tower_mid_x = tower_x + (tower_width / 2)
                    tower_mid_y = tower_y + (tower_height / 2)

                    min_x = min(selection_area_start[0], selection_area_end[0])
                    max_x = max(selection_area_start[0], selection_area_end[0])

                    # Determine the minimum and maximum y values
                    min_y = min(selection_area_start[1], selection_area_end[1])
                    max_y = max(selection_area_start[1], selection_area_end[1])

                    # Assuming tower_mid_x and tower_mid_y are the midpoint coordinates of the tower

                    if min_x <= tower_mid_x <= max_x and min_y <= tower_mid_y <= max_y and \
                            tower.owner is current_user:
                        selected_towers.append(tower)

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

    clicked = None
