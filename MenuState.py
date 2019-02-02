import pygame
import FastCreate as fastCreate
from State import *
from pygame.locals import *
from LevelState import *
from Display import *


class MenuState(State):
    selected = 0
    onSelect = False
    oldSelect = 0

    showControls = False

    showOptions = False
    optionSelected = 0
    onOptionsSelect = False
    widthOptions = 0
    heightOptions = 0

    showAbout = False

    def init(self, stateManager):

        self.title = pygame.image.load("Resources/Textures/title.png")
        self.selBackground = pygame.Surface((170, 35))
        self.selBackground.set_alpha(180)
        self.selBackground.fill(fastCreate.gray)

        self.menuBackground = pygame.Surface((340, 195))
        self.menuBackground.set_alpha(180)
        self.menuBackground.fill(fastCreate.gray)

        self.buttons = [
            fastCreate.makeText("New Game", stateManager.display.font, fastCreate.green, 30, 200),
            fastCreate.makeText("Controls", stateManager.display.font, fastCreate.green, 30, 240),
            fastCreate.makeText("Options", stateManager.display.font, fastCreate.green, 30, 280),
            fastCreate.makeText("About", stateManager.display.font, fastCreate.green, 30, 320),
            fastCreate.makeText("Quit", stateManager.display.font, fastCreate.green, 30, 360)
        ]
        widthControls = stateManager.display.width/2.5+10
        heightControls = stateManager.display.height/2.5
        self.controls = [
            fastCreate.makeText("Move: WASD or Arrows", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+30),
            fastCreate.makeText("Rotate: Mouse or QE", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+60),
            fastCreate.makeText("Fire: Mouse1 or SPACE", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+90),
            fastCreate.makeText("Open door: F", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+120),
            fastCreate.makeText("Switch gun: 1 and 2", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+150)
        ]

        if Settings.DIFFICULTY:
            self.difficulty = "Hard"
        else:
            self.difficulty = "Normal"
        if Settings.FULLSCREEN:
            self.fullscreen = "ON"
        else:
            self.fullscreen = "OFF"
        if Settings.MUSIC:
            self.music = "ON"
        else:
            self.music = "OFF"

        self.widthOptions = stateManager.display.width/2.5+20
        self.heightOptions = stateManager.display.height/2.5+30
        self.optionButtons = [
            fastCreate.makeText("Mouse Sensitivity: "+str(Settings.MOUSE_SENSITIVITY), stateManager.display.font,
                                fastCreate.green, self.widthOptions, self.heightOptions+0),
            fastCreate.makeText("Difficulty: "+self.difficulty, stateManager.display.font,
                                fastCreate.green, self.widthOptions, self.heightOptions+40),
            fastCreate.makeText("Fullscreen: "+self.fullscreen, stateManager.display.font,
                                fastCreate.green, self.widthOptions, self.heightOptions+80),
            fastCreate.makeText("Music: "+self.music, stateManager.display.font, fastCreate.green, self.widthOptions, self.heightOptions+120),
        ]
        self.abouts=[
            fastCreate.makeText("Collect the keys to", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+30),
            fastCreate.makeText("open the doors and", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+60),
            fastCreate.makeText("finish the game.", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+90),
            fastCreate.makeText("Raycasting game by", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+120),
            fastCreate.makeText("Kristijan Trajkovski", stateManager.display.fontMenu, fastCreate.white, widthControls, heightControls+150)
        ]
        # Play music
        # All Music is form Jan125
        # https://opengameart.org/users/jan125
        if Settings.MUSIC:
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
                elif event.key == K_RETURN:
                    self.__changeState(stateManager)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.onSelect:
                    self.__changeState(stateManager)
                elif self.onOptionsSelect:
                    pygame.mixer.pause()
                    pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/select.wav"))
                    self.__updateOptins(stateManager)

        mouseX, mouseY = pygame.mouse.get_pos()
        for i in range(len(self.buttons)):
            if self.buttons[i][1].collidepoint(mouseX, mouseY):
                self.selected = i
                self.selectSound()
                self.onSelect = True
                break
            self.onSelect = False
        if self.showOptions:
            for i in range(len(self.optionButtons)):
                if self.optionButtons[i][1].collidepoint(mouseX, mouseY):
                    self.optionSelected = i
                    self.onOptionsSelect = True
                    break
                self.onOptionsSelect = False

    def __changeState(self, stateManager):
        if self.selected == 0:
            self.showControls = False
            self.showOptions = False
            self.showAbout = False
            stateManager.pushState(LevelState())
        elif self.selected == 1:
            self.showControls = True
            self.showOptions = False
            self.showAbout = False
        elif self.selected == 2:
            self.showControls = False
            self.showOptions = True
            self.showAbout = False
        elif self.selected == 3:
            self.showControls = False
            self.showOptions = False
            self.showAbout = True
        elif self.selected == 4:
            fastCreate.terminate()

    def __updateOptins(self, stateManager):
        if self.optionSelected == 1:
            if Settings.DIFFICULTY:
                Settings.DIFFICULTY = 0
                self.difficulty = "Normal"
            else:
                self.difficulty = "Hard"
                Settings.DIFFICULTY = 1
            self.optionButtons[self.optionSelected] = fastCreate.makeText(
                "Difficulty: "+self.difficulty, stateManager.display.font, fastCreate.green, self.widthOptions, self.heightOptions+40)
        elif self.optionSelected == 0:
            if Settings.MOUSE_SENSITIVITY >= 20:
                Settings.MOUSE_SENSITIVITY = 0
            Settings.MOUSE_SENSITIVITY += 1
            self.optionButtons[self.optionSelected] = fastCreate.makeText(
                "Mouse Sensitivity: "+str(Settings.MOUSE_SENSITIVITY), stateManager.display.font, fastCreate.green, self.widthOptions, self.heightOptions+0)
        elif self.optionSelected == 2:
            if Settings.FULLSCREEN:
                Settings.FULLSCREEN = False
                self.fullscreen = "OFF"
                stateManager.display = Display(stateManager.display.width, stateManager.display.height)
            else:
                Settings.FULLSCREEN = True
                self.fullscreen = "ON"
                stateManager.display = Display(stateManager.display.width, stateManager.display.height, True)
            self.optionButtons[self.optionSelected] = fastCreate.makeText("Fullscreen: "+self.fullscreen, stateManager.display.font, fastCreate.green, self.widthOptions, self.heightOptions+80)
        elif self.optionSelected == 3:
            if Settings.MUSIC:
                Settings.MUSIC = False
                self.music = "OFF"
                pygame.mixer.music.pause()
            else:
                Settings.MUSIC = True
                self.music = "ON"
                pygame.mixer.music.unpause()
            self.optionButtons[self.optionSelected] = fastCreate.makeText("Music: "+self.music, stateManager.display.font, fastCreate.green, self.widthOptions, self.heightOptions+120)

    def update(self, delta, stateManager):
        pass

    def render(self, stateManager):
        stateManager.display.surface.fill(fastCreate.dark_gray)
        stateManager.display.surface.blit(pygame.image.load("Resources/Textures/sky1.png"), (-100, 0))
        stateManager.display.surface.blit(self.title, (0, 0))
        stateManager.display.surface.blit(self.selBackground, (25, 196+(self.selected*40)))
        if self.showControls:
            stateManager.display.surface.blit(self.menuBackground, (stateManager.display.width/2.5, 196))
            for control in self.controls:
                stateManager.display.surface.blit(control[0], control[1])
        if self.showOptions:
            stateManager.display.surface.blit(self.menuBackground, (stateManager.display.width/2.5, 196))
            for option in self.optionButtons:
                stateManager.display.surface.blit(option[0], option[1])
        if self.showAbout:
            stateManager.display.surface.blit(self.menuBackground, (stateManager.display.width/2.5, 196))
            for about in self.abouts:
                stateManager.display.surface.blit(about[0], about[1])
        for button in self.buttons:
            stateManager.display.surface.blit(button[0], button[1])

    def cleanUp(self):
        pass

    def selectSound(self):
        if self.selected != self.oldSelect:
            pygame.mixer.pause()
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/select.wav"))
        self.oldSelect = self.selected
