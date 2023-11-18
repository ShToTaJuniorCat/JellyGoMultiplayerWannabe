import pygame


class Obstacle:
    def __init__(self, vertices, color):
        """
        Initialize the Obstacle.

        Parameters:
        - vertices (list): List of (x, y) coordinates representing the vertices of the obstacle.
        - color (tuple): RGB color tuple (e.g., (255, 0, 0) for red).
        """
        self.vertices = vertices
        self.color = color

    def collides_with_obstacle(self, point):
        """
        Check if a given point collides with the obstacle.

        Parameters:
        - point (tuple): (x, y) coordinates of the point to check.

        Returns:
        - bool: True if the point is inside the obstacle, False otherwise.
        """
        x, y = point
        odd_nodes = False
        j = len(self.vertices) - 1

        for i in range(len(self.vertices)):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]

            if (yi < y <= yj) or (yj < y <= yi):
                if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                    odd_nodes = not odd_nodes

            j = i

        return odd_nodes

    def draw(self, surface):
        """
        Draw the obstacle on a Pygame surface.

        Parameters:
        - surface (pygame.Surface): Pygame surface to draw the obstacle on.
        """
        temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.polygon(temp_surface, self.color, self.vertices)

        # Set alpha value for transparency (adjust the alpha value as needed)
        alpha_value = 128  # You can modify this value to control transparency (0 to 255)
        temp_surface.set_alpha(alpha_value)

        surface.blit(temp_surface, (0, 0))