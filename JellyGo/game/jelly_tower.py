import pygame
from time import time
from constants import TOWER_CONSTANTS, BACKGROUND_COLOR


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
                 tower_type: str):
        """
        Initialize a JellyTower object.

        Parameters:
        - level (int): An integer representing the tower's level (1 to 5).
        - owner (Player): A reference to the player who owns the tower.
        - current_jellies (float): A float representing the current number of jellies in the tower.
        - max_jellies (int): An integer representing the maximum jelly capacity of the tower.
        - protection_factor (float): A float representing the tower's protection factor.
        - sending_speed (int): An integer representing the tower's sending speed.
        - production_speed (float): A float representing the tower's production speed.
        - tower_image (str): A string representing the path to the tower_image of the tower's graphical representation.
        """
        super().__init__()
        self.tower_image = pygame.image.load(fr"../assets/images/towers/{tower_type}/level_{level}.png")
        self.image = pygame.Surface((self.tower_image.get_width() + 5, self.tower_image.get_height()))
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
        try:
            self.time_between_production = 1 / production_speed
        except ZeroDivisionError:
            self.time_between_production = 99999999

    def upgrade(self):
        # Check if the tower is upgradable
        if not self.is_upgradable():
            return False

        # Increment the level
        self.level += 1

        # Retrieve the tower's attributes from the constant dictionary
        attributes = TOWER_CONSTANTS[self.tower_type][self.level]

        # Unpack the attributes into respective variables
        self.protection_factor, self.sending_speed, self.production_speed, self.max_jellies, _ = attributes
        self.tower_image = pygame.image.load(fr"../assets/images/towers/{self.tower_type}/level_{self.level}.png")

        # Deduct the upgrade cost from the player's jellies
        self.current_jellies -= self.upgrade_cost
        self.upgrade_cost = TOWER_CONSTANTS[self.tower_type][self.level][4]

    def is_upgradable(self):
        return self.current_jellies > self.upgrade_cost and self.level < len(TOWER_CONSTANTS[self.tower_type])

    def draw(self, surface: pygame.Surface):
        # # Set the position of the tower on the surface
        # tower_rect = self.tower_image.get_rect()
        # tower_rect.topleft = (self.tower_x, self.tower_y)
        # self.image_rect = tower_rect
        #
        # # Remove any previously drawings here
        # pygame.draw.rect(surface, BACKGROUND_COLOR, (self.tower_x,
        #                                              self.tower_y,
        #                                              tower_rect.width,
        #                                              tower_rect.height))
        #
        # # Draw the tower tower_image on the surface
        # surface.blit(self.tower_image, tower_rect)
        #
        # # Display the current number of jellies (centered on the tower)
        # jellies_text = pygame.font.Font(None, 36).render(str(int(self.current_jellies)), True, (255, 255, 255))
        # jellies_rect = jellies_text.get_rect()
        # jellies_rect.center = tower_rect.center  # Center the text on the tower
        # surface.blit(jellies_text, jellies_rect)



        # Create a surface for the jellies bar and fill it with the owner's color
        jellies_bar_surface = pygame.Surface((10, jellies_bar_height))
        jellies_bar_surface.fill(self.owner.color)

        # Set the position of the jellies bar on the tower's bottom-center
        jellies_bar_rect = jellies_bar_surface.get_rect()
        jellies_bar_rect.bottom = tower_rect.bottom
        jellies_bar_rect.left = tower_rect.left

        # Draw the jellies bar on the surface
        surface.blit(jellies_bar_surface, jellies_bar_rect)

        pygame.display.update()

    def tick(self, surface: pygame.Surface):
        self.upgrade()

        # self.draw(surface)
        self.update_image()

        if self.last_produced + self.time_between_production <= time():
            self.produce_jelly()

    def update_image(self):
        self.tower_image = pygame.image.load(fr"../assets/images/towers/{self.tower_type}/level_{self.level}.png")
        self.image = pygame.Surface((self.tower_image.get_width() + 5, self.tower_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.tower_x, self.tower_y)

        self.image.blit(self.tower_image, (0, 0))

        # Display the current number of jellies (centered on the tower)
        jellies_text = pygame.font.Font(None, 36).render(str(int(self.current_jellies)), True, (255, 255, 255))
        jellies_rect = jellies_text.get_rect()
        jellies_rect.center = self.rect.center  # Center the text on the tower
        self.image.blit(jellies_text, jellies_rect)

        # Calculate the height of the jellies bar
        jellies_bar_height = (self.current_jellies / self.max_jellies)
        jellies_bar_height = max(0.1, min(0.9, jellies_bar_height))  # height gotta be between 10%-90%
        jellies_bar_height = int(jellies_bar_height * self.rect.height)

        jellies_bar = pygame.Rect(0, 0, 10, jellies_bar_height)
        jellies_bar.bottomleft = (0, self.rect.height)

        pygame.draw.rect(self.image, self.owner.color, jellies_bar)

    def produce_jelly(self):
        self.last_produced = time()

        if self.current_jellies < self.max_jellies:
            self.current_jellies += 1
            return

        elif self.current_jellies > self.max_jellies:
            self.current_jellies -= 1

        if int(self.current_jellies) == self.max_jellies:
            self.current_jellies = self.max_jellies
