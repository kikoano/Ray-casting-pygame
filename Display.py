import pygame

class Display:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        # Create display
        self.surface = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Delta of combat")
        pygame.display.set_icon(pygame.image.load("Resources/Textures/icon.ico"))
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.fontHud = pygame.font.Font('freesansbold.ttf', 20)
