import pygame
from constants import *
from time import time


class JellyBubble(pygame.sprite.Sprite):
    def __init__(self, path: list, speed: int, owner, amount: int, target_tower):
        self.path = path
        self.path_point_position = 0
        self.speed = 1/speed
        self.owner = owner
        self.amount = amount
        self.target_tower = target_tower

        self.bubble_x = path[self.path_point_position][0]
        self.bubble_y = path[self.path_point_position][1]

        super().__init__()
        self.bubble_image = pygame.image.load(fr"../assets/images/towers/house/level_1.png")
        self.tower_image = self.scale_image_in_ratio(self.bubble_image, JELLY_BUBBLE_WIDTH).convert_alpha()
        self.image = pygame.Surface((self.bubble_image.get_width(),
                                     self.bubble_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.bubble_x, self.bubble_y)

        self.dirty = True
        self.layer = 1

        self.last_moved = 0
        self.reached_destination = False

    @staticmethod
    def scale_image_in_ratio(pygame_image: pygame.Surface, destination_width: int):
        """
        Scale a given python image or surface to have a destined width, while maintaining it's ratio.

        :param pygame_image: pygame Surface object to scale
        :param destination_width: Destined width for the Surface
        :return: pygame.Surface
        """
        destination_height = (pygame_image.get_height() * destination_width) / pygame_image.get_width()

        return pygame.transform.scale(pygame_image, (destination_width, destination_height))

    def tick(self):
        self.update_image()

        if self.last_moved + self.speed <= time():
            self.move_along_path()

        self.dirty = True

    def update_image(self):
        self.rect = self.image.get_rect()
        self.rect.center = (self.bubble_x, self.bubble_y)

        self.image.blit(self.bubble_image, (0,
                                            self.rect.height - self.bubble_image.get_height()))

        # Display the current number of jellies (centered on the tower's center)
        font_size = int((36 - ((len(str(int(self.amount))) - 1) * 5)) * (JELLY_BUBBLE_WIDTH / 20))
        jellies_text = pygame.font.Font(None, font_size).render(str(int(self.amount)), True, (255, 255, 255))
        # Calculate the position for blitting jellies_text at the center of self.image
        text_width, text_height = jellies_text.get_size()
        image_width, image_height = self.image.get_size()
        # Blit the jellies_text onto self.image at the calculated position
        self.image.blit(jellies_text, ((image_width - text_width) // 2 - 2,
                                       image_height - JELLY_BUBBLE_TEXT_CENTER))

        # Set the alpha transparency flag
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))  # Set the background color to be transparent
        self.image.set_alpha(255)  # You can adjust the alpha value as needed

    def move_along_path(self):
        self.last_moved = time()

        self.path_point_position += 1
        if len(self.path) == self.path_point_position:
            self.reached_destination = True
        else:
            self.bubble_x, self.bubble_y = self.path[self.path_point_position]
