import pygame

class Display:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        # Create display
        self.surface = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Raycasting demo")
