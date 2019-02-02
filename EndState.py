import pygame
import FastCreate as fastCreate
from State import *
from pygame.locals import *
from LevelState import *


class EndState(State):
    select = False
    alreadySelected = False

    def __init__(self, player):
        self.player = player

    def init(self, stateManager):
        self.selBackground = pygame.Surface((170, 35))
        self.selBackground.set_alpha(180)
        self.selBackground.fill(fastCreate.gray)
        self.scoreBackground = pygame.Surface((300, 270))
        self.scoreBackground.set_alpha(180)
        self.scoreBackground.fill(fastCreate.gray)
        self.mainMenu = fastCreate.makeText("Main Menu", stateManager.display.font, fastCreate.green,
                                            stateManager.display.width/2-85, stateManager.display.height-80)
        # Play music
        if Settings.MUSIC:
            pygame.mixer.music.load("Resources/Sounds/Music/twentyone.ogg")
            pygame.mixer.music.play(-1)
        scoreWidth = stateManager.display.width/2-140
        scoreHeight = stateManager.display.height-380
        if not self.player.alive:
            resultStr = "You Died!"
        else:
            resultStr = "You Won!"
        self.scores = [
            fastCreate.makeText(resultStr, stateManager.display.fontResult, fastCreate.red, scoreWidth+50, scoreHeight-60),
            fastCreate.makeText("Kills:       "+str(self.player.kills), stateManager.display.fontScore, fastCreate.white, scoreWidth, scoreHeight),
            fastCreate.makeText("Shots:       "+str(self.player.shots), stateManager.display.fontScore, fastCreate.white, scoreWidth, scoreHeight+40),
            fastCreate.makeText("Aim shots:   "+str(self.player.aimShots), stateManager.display.fontScore,fastCreate.white, scoreWidth, scoreHeight+80),
            fastCreate.makeText("Miss shots:  "+str(self.player.shots - self.player.aimShots),stateManager.display.fontScore, fastCreate.white, scoreWidth, scoreHeight+120),
            fastCreate.makeText("Health pick: "+str(self.player.healthPick), stateManager.display.fontScore,fastCreate.white, scoreWidth, scoreHeight+160),
            fastCreate.makeText("Ammo pick:   "+str(self.player.ammoPick), stateManager.display.fontScore,fastCreate.white, scoreWidth, scoreHeight+200)
        ]

    def handleKeyEvents(self, stateManager):
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                fastCreate.terminate()
            elif event.type == KEYDOWN:
                if event.key in (K_RETURN, K_ESCAPE):
                    stateManager.popState()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.select:
                stateManager.popState()

        mouseX, mouseY = pygame.mouse.get_pos()
        if self.mainMenu[1].collidepoint(mouseX, mouseY):
            self.select = True
            self.selectSound()
        else:
            self.select = False
            self.alreadySelected = False

    def update(self, delta, stateManager):
        pass

    def render(self, stateManager):
        stateManager.display.surface.fill(fastCreate.dark_gray)
        stateManager.display.surface.blit(pygame.image.load("Resources/Textures/sky1.png"), (-100, 0))
        stateManager.display.surface.blit(self.mainMenu[0], self.mainMenu[1])
        if self.select:
            stateManager.display.surface.blit(self.selBackground, (stateManager.display.width/2-93, stateManager.display.height-84))
        stateManager.display.surface.blit(self.scoreBackground, (stateManager.display.width/2-150, stateManager.display.height-400))
        for score in self.scores:
            stateManager.display.surface.blit(score[0], score[1])

    def cleanUp(self):
        pass

    def selectSound(self):
        if not self.alreadySelected:
            pygame.mixer.pause()
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/select.wav"))
            self.alreadySelected = True
