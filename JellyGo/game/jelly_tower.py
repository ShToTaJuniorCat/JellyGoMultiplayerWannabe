import pygame
from time import time
from constants import *


class JellyTower(pygame.sprite.Sprite):
    def __init__(self, tower_x: int,
                 tower_y: int,
                 level: int,
                 owner,
                 current_jellies: float,
                 max_jellies: int,
                 protection_factor: float,
                 sending_speed: int,
                 production_speed: float,
                 tower_type: str,
                 is_current_player: bool,
                 layer: int = 1):
        """
        Initialize a JellyTower object.

        Parameters:
        - level (int): An integer representing the tower1's level (1 to 5).
        - owner (Player): A reference to the player who owns the tower1.
        - current_jellies (float): A float representing the current number of jellies in the tower1.
        - max_jellies (int): An integer representing the maximum jelly capacity of the tower1.
        - protection_factor (float): A float representing the tower1's protection factor.
        - sending_speed (int): An integer representing the tower1's sending speed.
        - production_speed (float): A float representing the tower1's production speed.
        - tower_image (str): A string representing the path to the tower_image of the tower1's graphical representation.
        """
        super().__init__()
        self.tower_image = pygame.image.load(fr"../assets/images/towers/{tower_type}/level_{level}.png")
        self.tower_image = self.scale_image_in_ratio(self.tower_image, TOWERS_WIDTH).convert_alpha()
        self.image = pygame.Surface((self.tower_image.get_width() + 5,
                                     self.tower_image.get_height() + ATTRIBUTES_SURFACE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (tower_x, tower_y)

        self.tower_x = tower_x
        self.tower_y = tower_y
        self.level = level
        self.owner = owner
        self.current_jellies = current_jellies
        self.max_jellies = max_jellies
        self.protection_factor = protection_factor
        self.sending_speed = sending_speed
        self.production_speed = production_speed
        self.upgrade_cost = TOWER_CONSTANTS[tower_type][level][4]
        self.tower_type = tower_type
        self.last_produced = 0
        self.hovered = False
        self.click_position = None
        self.dirty = True
        self.layer = layer
        self.is_current_player = is_current_player
        try:
            self.time_between_production = 1 / production_speed
        except ZeroDivisionError:
            self.time_between_production = 99999999

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

    def get_tower_bounding_box(self):
        return self.tower_image.get_bounding_rect()\
            .move(self.rect.topleft[0],
                  self.rect.topleft[1] + UPGRADE_BUTTON_SIZE + UPGRADE_BUTTON_MARGIN)

    def get_bounding_box(self):
        return self.image.get_bounding_rect().move(self.rect.topleft)

    def upgrade(self):
        # Check if the tower1 is upgradable
        if not self.is_upgradable():
            return False

        # Increment the level
        self.level += 1

        # Retrieve the tower1's attributes from the constant dictionary
        attributes = TOWER_CONSTANTS[self.tower_type][self.level]

        # Unpack the attributes into respective variables
        self.protection_factor, self.sending_speed, self.production_speed, self.max_jellies, _ = attributes
        # Update tower production intervals
        try:
            self.time_between_production = 1 / self.production_speed
        except ZeroDivisionError:
            self.time_between_production = 99999999

        # Deduct the upgrade cost from the player's jellies
        self.current_jellies -= self.upgrade_cost
        self.upgrade_cost = TOWER_CONSTANTS[self.tower_type][self.level][4]

    def is_upgradable(self):
        if self.tower_type == "house":
            return False

        return self.current_jellies >= self.upgrade_cost and self.level < len(TOWER_CONSTANTS[self.tower_type])

    def tick(self):
        self.update_image()

        # self.upgrade()

        if self.last_produced + self.time_between_production <= time():
            self.produce_jelly()

        self.dirty = True

    def update_image(self):
        self.tower_image = pygame.image.load(fr"../assets/images/towers/{self.tower_type}/level_{self.level}.png")
        self.tower_image = self.scale_image_in_ratio(self.tower_image, TOWERS_WIDTH).convert_alpha()
        self.image = pygame.Surface((self.tower_image.get_width() + 5,
                                     self.tower_image.get_height() +
                                     UPGRADE_BUTTON_SIZE +
                                     (UPGRADE_BUTTON_SIZE / 4) +
                                     ATTRIBUTES_SURFACE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.tower_x, self.tower_y)

        self.image.blit(self.tower_image, (0,
                                           self.rect.height - self.tower_image.get_height() - ATTRIBUTES_SURFACE_HEIGHT))

        # Display the current number of jellies (centered on the tower's center)
        font_size = int((36 - ((len(str(int(self.current_jellies))) - 1) * 5)) * (TOWERS_WIDTH / 50))
        jellies_text = pygame.font.Font(None, font_size).render(str(int(self.current_jellies)), True, (255, 255, 255))
        # Calculate the position for blitting jellies_text at the center of self.image
        text_width, text_height = jellies_text.get_size()
        image_width, image_height = self.image.get_size()
        # Blit the jellies_text onto self.image at the calculated position
        self.image.blit(jellies_text, ((image_width - text_width) // 2 - 2,
                                       image_height - TOWERS_TEXT_CENTER - ATTRIBUTES_SURFACE_HEIGHT))

        # Calculate the height of the jellies bar
        jellies_bar_height = (self.current_jellies / self.max_jellies)
        jellies_bar_height = max(0.1, min(0.9, jellies_bar_height))  # height gotta be between 10%-90%
        jellies_bar_height = int(jellies_bar_height * self.tower_image.get_height())

        jellies_bar = pygame.Rect(0, 0, 10, jellies_bar_height)
        jellies_bar.bottomleft = (0, image_height - ATTRIBUTES_SURFACE_HEIGHT)

        pygame.draw.rect(self.image, self.owner.color, jellies_bar)

        # Display upgrade indicator
        if self.is_upgradable() and self.is_current_player:
            upgrade_indicator_image = pygame.image.load(r"../assets/images/icons/upgrade_indicator.png")
            upgrade_indicator_image = self.scale_image_in_ratio(upgrade_indicator_image,
                                                                UPGRADE_INDICATOR_SIZE).convert_alpha()
            self.image.blit(upgrade_indicator_image, (self.rect.width - upgrade_indicator_image.get_width(),
                                                      self.rect.height - upgrade_indicator_image.get_height() -
                                                      ATTRIBUTES_SURFACE_HEIGHT))

        # Display upgrade button and tower specifications
        if self.hovered:
            if self.is_current_player:
                # Display upgrade button
                upgrade_image = pygame.image.load(fr"../assets/images/icons/upgrade/{self.is_upgradable()}_upgrade.png")
                upgrade_image = pygame.transform.scale(upgrade_image,
                                                       (UPGRADE_BUTTON_SIZE, UPGRADE_BUTTON_SIZE)).convert_alpha()
                self.image.blit(upgrade_image, ((image_width - upgrade_image.get_width()) // 2 - UPGRADE_BUTTON_MARGIN, 0))

                # Handle mouse clicks
                if self.click_position:
                    upgrade_image_x_range = range(int((image_width - upgrade_image.get_width()) / 2) +
                                                  self.tower_x - self.image.get_width(),
                                                  int((image_width - upgrade_image.get_width()) / 2) +
                                                  self.tower_x - self.image.get_width() + UPGRADE_BUTTON_SIZE)

                    upgrade_image_y_range = range(self.tower_y - self.image.get_height(),
                                                  self.tower_y - self.image.get_height() + UPGRADE_BUTTON_SIZE)

                    if self.click_position[0] in upgrade_image_x_range and self.click_position[1] in upgrade_image_y_range:
                        self.upgrade()

                    self.click_position = None

            # Display tower attributes
            attributes_surface = pygame.Surface((ATTRIBUTES_SURFACE_WIDTH, ATTRIBUTES_SURFACE_HEIGHT))

            # Attributes background
            pygame.draw.rect(attributes_surface, (1, 1, 1),
                             pygame.Rect(0, 0, ATTRIBUTES_SURFACE_WIDTH, ATTRIBUTES_SURFACE_HEIGHT),
                             int(ATTRIBUTES_SURFACE_HEIGHT / 2) + 1, 3)

            # Production speed
            attr_image = pygame.image.load(r"../assets/images/icons/tower_attributes/production.png").convert_alpha()
            attr_image = pygame.transform.scale(attr_image, (ATTRIBUTES_ICON_SIZE, ATTRIBUTES_ICON_SIZE))
            attributes_surface.blit(attr_image,
                                    (attributes_surface.get_width() / 5 - ATTRIBUTES_ICON_SIZE,
                                     attributes_surface.get_height() / 2 - 1.5 * ATTRIBUTES_ICON_SIZE))
            # Text
            font_size = int(ATTRIBUTES_SURFACE_HEIGHT / 2)
            attr_text = pygame.font.Font(None, font_size).render(str(self.production_speed), True,
                                                                    (255, 255, 255))
            # Blit the jellies_text onto self.image at the calculated position
            attributes_surface.blit(attr_text, (attr_image.get_rect().topright[0] + 10,
                                                attributes_surface.get_height() / 2 - 1.5 * ATTRIBUTES_ICON_SIZE))

            self.image.blit(attributes_surface, (0, image_height - ATTRIBUTES_SURFACE_HEIGHT))

            # Storage capacity
            attr_image = pygame.image.load(r"../assets/images/icons/tower_attributes/capacity.png").convert_alpha()
            attr_image = pygame.transform.scale(attr_image, (ATTRIBUTES_ICON_SIZE, ATTRIBUTES_ICON_SIZE))
            attributes_surface.blit(attr_image,
                                    (4 * attributes_surface.get_width() / 5 - 1.5 * ATTRIBUTES_ICON_SIZE,
                                     attributes_surface.get_height() / 2 - 1.5 * ATTRIBUTES_ICON_SIZE))
            # Text
            attr_text = pygame.font.Font(None, font_size).render(str(int(self.max_jellies)), True,
                                                                    (255, 255, 255))
            # Blit the jellies_text onto self.image at the calculated position
            attributes_surface.blit(attr_text, (4 * attributes_surface.get_width() / 5 - 0.2 * ATTRIBUTES_ICON_SIZE,
                                                attributes_surface.get_height() / 2 - 1.3 * ATTRIBUTES_ICON_SIZE))

            self.image.blit(attributes_surface, (0, image_height - ATTRIBUTES_SURFACE_HEIGHT))

            # Protection speed
            attr_image = pygame.image.load(r"../assets/images/icons/tower_attributes/shield.png").convert_alpha()
            attr_image = pygame.transform.scale(attr_image, (ATTRIBUTES_ICON_SIZE, ATTRIBUTES_ICON_SIZE))
            attributes_surface.blit(attr_image,
                                    (attributes_surface.get_width() / 5 - ATTRIBUTES_ICON_SIZE,
                                     attributes_surface.get_height() - 1.5 * ATTRIBUTES_ICON_SIZE))
            # Text
            font_size = int(ATTRIBUTES_SURFACE_HEIGHT / 2)
            attr_text = pygame.font.Font(None, font_size).render(str(int(self.protection_factor)), True,
                                                                 (255, 255, 255))
            # Blit the jellies_text onto self.image at the calculated position
            attributes_surface.blit(attr_text, (attr_image.get_rect().topright[0] + 10,
                                                attributes_surface.get_height() - 1.5 * ATTRIBUTES_ICON_SIZE))

            self.image.blit(attributes_surface, (0, image_height - ATTRIBUTES_SURFACE_HEIGHT))

            # Sending speed
            attr_image = pygame.image.load(r"../assets/images/icons/tower_attributes/speed.png").convert_alpha()
            attr_image = pygame.transform.scale(attr_image, (ATTRIBUTES_ICON_SIZE, ATTRIBUTES_ICON_SIZE))
            attributes_surface.blit(attr_image,
                                    (4 * attributes_surface.get_width() / 5 - 1.5 * ATTRIBUTES_ICON_SIZE,
                                     attributes_surface.get_height() - 1.5 * ATTRIBUTES_ICON_SIZE))
            # Text
            font_size = int(ATTRIBUTES_SURFACE_HEIGHT / 2)
            attr_text = pygame.font.Font(None, font_size).render(str(int(self.sending_speed)), True,
                                                                 (255, 255, 255))
            # Blit the jellies_text onto self.image at the calculated position
            attributes_surface.blit(attr_text, (4 * attributes_surface.get_width() / 5 - 0.2 * ATTRIBUTES_ICON_SIZE,
                                                attributes_surface.get_height() - 1.5 * ATTRIBUTES_ICON_SIZE))

            self.image.blit(attributes_surface, (0, image_height - ATTRIBUTES_SURFACE_HEIGHT))

        # Set the alpha transparency flag
        self.image = self.image.convert()
        self.image.set_colorkey((0, 0, 0))  # Set the background color to be transparent
        self.image.set_alpha(255)  # You can adjust the alpha value as needed

    def produce_jelly(self):
        self.last_produced = time()

        if self.current_jellies < self.max_jellies:
            self.current_jellies += 1
            return

        elif self.current_jellies > self.max_jellies:
            self.current_jellies -= 1

        if int(self.current_jellies) == self.max_jellies:
            self.current_jellies = self.max_jellies
