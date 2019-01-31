import pygame
import FastCreate as fastCreate
from State import *
from pygame.locals import *
from LevelState import *


class MenuState(State):

    selected = 0
    oldSelect = 0

    def init(self, stateManager):

        self.title = pygame.image.load("Resources/Textures/title.png")
        self.selBackground = pygame.Surface((170, 35))
        self.selBackground.set_alpha(200)
        self.selBackground.fill(fastCreate.gray)
        self.buttons = [
            fastCreate.makeText("New Game", stateManager.display.font, fastCreate.green, 30, 200),
            fastCreate.makeText("Controls", stateManager.display.font, fastCreate.green, 30, 240),
            fastCreate.makeText("Options", stateManager.display.font, fastCreate.green, 30, 280),
            fastCreate.makeText("About", stateManager.display.font, fastCreate.green, 30, 320),
            fastCreate.makeText("Quit", stateManager.display.font, fastCreate.green, 30, 360)
        ]
        # Play music
        # All Music is form Jan125
        # https://opengameart.org/users/jan125
        pygame.mixer.music.load("Resources/Sounds/Music/twentyone.ogg")
        pygame.mixer.music.play(-1)

    def handleKeyEvents(self, stateManager):
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                fastCreate.terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w) and self.selected > 0:
                    self.selected -= 1
                    self.selectSound()
                elif event.key in (K_DOWN, K_s) and self.selected < len(self.buttons)-1:
                    self.selected += 1
                    self.selectSound()
                elif event.key == K_ESCAPE:
                    fastCreate.terminate()
                elif event.key in (K_SPACE, K_RETURN):
                    self.__changeState(stateManager)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.__changeState(stateManager)

        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(len(self.buttons)):
            if self.buttons[i][1].collidepoint(mouseX, mouseY):
                self.selected = i
                self.selectSound()

    def __changeState(self, stateManager):
        if self.selected == 0:
            stateManager.pushState(LevelState())
        elif self.selected == 4:
            fastCreate.terminate()

    def update(self, delta, stateManager):
        pass

    def render(self, stateManager):
        stateManager.display.surface.fill(fastCreate.dark_gray)
        stateManager.display.surface.blit(pygame.image.load("Resources/Textures/sky1.png"), (-100, 0))
        stateManager.display.surface.blit(self.title, (0, 0))
        stateManager.display.surface.blit(self.selBackground, (25, 196+(self.selected*40)))
        for button in self.buttons:
            stateManager.display.surface.blit(button[0], button[1])
    def cleanUp(self):
        pass
    def selectSound(self):
        if self.selected != self.oldSelect:
            pygame.mixer.pause()
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/select.wav"))
        self.oldSelect = self.selected
