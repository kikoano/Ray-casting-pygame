import pygame

class Display:
    def __init__(self,width,height,fullscreen=False):
        self.width = width
        self.height = height
        # Create display
        if fullscreen:
            self.surface = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Delta of combat")
        pygame.display.set_icon(pygame.image.load("Resources/Textures/icon.ico"))
        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.fontScore = pygame.font.Font('Resources/Fonts/CONSOLAB.ttf', 30)
        self.fontMenu = pygame.font.Font('Resources/Fonts/CONSOLAB.ttf', 28)
        self.fontResult = pygame.font.Font('Resources/Fonts/CONSOLAB.ttf', 40)
        self.fontHud = pygame.font.Font('freesansbold.ttf', 20)
