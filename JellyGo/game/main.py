from os import environ
import pygame
from jelly_tower import JellyTower
from player import Player
from constants import *
from obstacle import Obstacle
import numpy as np
from pathfinder import a_star_search
from jelly_buble import JellyBubble
from concurrent.futures import ThreadPoolExecutor
from functools import partial


environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (WINDOW_POSITION_X, WINDOW_POSITION_Y)


def compress_map(compression_factor, input_map):
    rows = len(input_map)
    cols = len(input_map[0])

    # Create an output map with dimensions reduced by the compression factor
    compressed_rows = (rows + compression_factor - 1) // compression_factor
    compressed_cols = (cols + compression_factor - 1) // compression_factor
    output_map = [[0] * compressed_cols for _ in range(compressed_rows)]

    for i in range(0, rows, compression_factor):
        for j in range(0, cols, compression_factor):
            # Extract the pixel group
            pixel_group = [input_map[x][y] for x in range(i, min(i + compression_factor, rows)) for y in range(j, min(j + compression_factor, cols))]

            # Count the occurrences of 0 and 1 in the pixel group
            count_0 = pixel_group.count(0)
            count_1 = pixel_group.count(1)

            # Determine the dominant pixel value
            dominant_pixel = 0 if count_0 > count_1 else 1

            # Set the value of the pixel in the compressed map
            compressed_row = i // compression_factor
            compressed_col = j // compression_factor
            output_map[compressed_row][compressed_col] = dominant_pixel

    return output_map


def is_point_inside_polygon(x, y, vertices):
    # Ray casting algorithm
    intersections = 0
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]

        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            intersections += 1

    return intersections % 2 == 1


def convert_returned_path_to_usable(tuple_list):
    return [(COMPRESSION_FACTOR * y, COMPRESSION_FACTOR * x) for x, y in tuple_list]


def process_tower(sending_tower, receiving_tower, amount, local_pixel_map):
    print(f"Sending tower {sending_tower}")
    amount_sent = sending_tower.send_jellies(amount)
    path = convert_returned_path_to_usable(a_star_search(
        local_pixel_map, tuple(int(value / COMPRESSION_FACTOR) for value in sending_tower.rect.center),
        tuple(int(value / COMPRESSION_FACTOR) for value in receiving_tower.rect.center)))
    bubble = JellyBubble(path, sending_tower.sending_speed, sending_tower.owner, amount_sent, receiving_tower)
    jelly_bubble_group.add(bubble)


def send_jellies(sending_towers, receiving_tower, amount):
    local_pixel_map = screen_pixels
    for tower in sending_towers + [receiving_tower]:
        # Get the tower's bounding box
        tower_rect = tower.get_tower_bounding_box()

        # Iterate through the bounding box and mark pixels within the tower
        for x in range(tower_rect.left, tower_rect.right):
            for y in range(tower_rect.top, tower_rect.bottom):
                local_pixel_map[y][x] = 1  # Mark this pixel as walkable path

    compressed_pixel_map = compress_map(COMPRESSION_FACTOR, local_pixel_map)

    # Display jelly sending animation
    # Create partially bound function
    partial_process_tower = partial(process_tower, receiving_tower=receiving_tower, amount=amount,
                                    local_pixel_map=compressed_pixel_map)

    # Call the ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        executor.map(partial_process_tower, sending_towers)


# Initialize pygame screen
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jelly Go")
image_width, image_height = screen.get_size()

# Load the background image
background_image = pygame.image.load(r"../assets/images/background.jpg")
background_image = pygame.transform.scale(background_image, (image_width, image_height))  # Scale to fit background
screen.blit(background_image, (0, 0))  # Place it in the top-left corner

tower_group = pygame.sprite.LayeredUpdates()  # Create sprite groups and enable the layered flag

# Initialize players
neutral_player = Player(GRAY, "NEUTRAL-PLAYER")  # Neutral player is always gray
red_player = Player(RED, "RED-PLAYER")  # Enemy
current_user = Player(BLUE, "BLUE-PLAYER")  # Current playing user (usually blue for testing)

# Neutral player's towers
neutral_player_towers = [
    # JellyTower(tower_x=265, tower_y=220, level=1, owner=neutral_player, current_jellies=20.0,
    #            max_jellies=10, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="barracks", is_current_player=False),  # top first
    # JellyTower(tower_x=250, tower_y=950, level=1, owner=neutral_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="fort", is_current_player=False),  # bottom first
    # JellyTower(tower_x=1020, tower_y=220, level=1, owner=neutral_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="house", is_current_player=False)  # top third
]

# Red player's towers
red_player_towers = [
    # JellyTower(tower_x=1370, tower_y=220, level=1, owner=red_player, current_jellies=20.0,
    #            max_jellies=10, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="barracks", is_current_player=False),  # top fourth
    # JellyTower(tower_x=1350, tower_y=600, level=1, owner=red_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="barracks", is_current_player=False),  # middle fourth
    # JellyTower(tower_x=1350, tower_y=950, level=1, owner=red_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="house", is_current_player=False),  # bottom fourth
    # JellyTower(tower_x=1015, tower_y=950, level=1, owner=red_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="lab", is_current_player=False),  # bottom third
    # JellyTower(tower_x=1015, tower_y=600, level=1, owner=red_player, current_jellies=50.0,
    #            max_jellies=50, protection_factor=1, sending_speed=50, production_speed=0.4,
    #            tower_type="fort", is_current_player=False),  # middle third
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

obst = Obstacle([(110, 85), (356, 470), (314, 306), (368, 47), (315, 212)], RED)
obst1 = Obstacle([(64, 220), (239, 430), (141, 422), (80, 522), (450, 800)], RED)
obst3 = Obstacle([(35, 505), (25, 505), (25, 495), (35, 495)], RED)
obstacles_list = [obst]

# Find screen pixel's state: 0 for possible passage, 1 for no passage
screen_pixels = np.ones((SCREEN_HEIGHT, SCREEN_WIDTH))

for obstacle in obstacles_list:
    vertices = obstacle.vertices

    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)

    for x in range(max(0, min_x), min(SCREEN_WIDTH, max_x) + 1):
        for y in range(max(0, min_y), min(SCREEN_HEIGHT, max_y) + 1):
            if is_point_inside_polygon(x, y, vertices):
                screen_pixels[y][x] = 0

    for player_towers in towers_by_player:
        for tower in player_towers:
            # Get the tower's bounding box
            tower_rect = tower.get_tower_bounding_box(False)

            # Iterate through the bounding box and mark pixels within the tower
            for x in range(tower_rect.left, tower_rect.left + TOWERS_WIDTH):
                for y in range(tower_rect.top, tower_rect.top + tower_rect.height):
                    screen_pixels[y][x] = 0  # Mark this pixel as within a tower

jelly_bubble_group = pygame.sprite.LayeredUpdates()

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

    for jelly_bubble in jelly_bubble_group:
        jelly_bubble.tick()
        if jelly_bubble.reached_destination:
            target_tower = jelly_bubble.target_tower

            # If the owner of the bubble and the tower are the same, multiply amount by 1 (add jellies)
            # otherwise, multiply by -1 (decrease jellies)
            # Done by very stupid arithmetics cuz i'm too lazy to make an if statement
            target_tower.receive_jellies(jelly_bubble.amount * ((
                (2 * int(jelly_bubble.owner == target_tower.owner)) - 1)))

            jelly_bubble_group.remove(jelly_bubble)

    jelly_bubble_group.clear(screen, screen)
    jelly_bubble_group.draw(screen)

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

    for obstacle in obstacles_list:
        obstacle.draw(screen)

    clicked = None
