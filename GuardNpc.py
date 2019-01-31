from Sprite import *
from Texture import *
import pygame


class GuardNpc(Sprite):
    health = 3
    damage = 2
    idleImage = Texture("guardIdle.png", True)
    currentImage = idleImage

    deadSprites = [
        Texture("guardDead1.png", True),
        Texture("guardDead2.png", True),
        Texture("guardDead3.png", True),
        Texture("guardDead4.png", True),
        Texture("guardDead5.png", True)
    ]
    timePassed = 0
    stayDeadTime = 10 
    deadAnimTime = 1
    startDeadAnim = False

    def __init__(self, posX, posY, texture, block=False):
        super().__init__(posX, posY, texture, block)

    def update(self, delta, stateManager):
        
        if self.health <= 0 and not self.startDeadAnim:
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/enemyDeath.wav"))
            self.startDeadAnim = True
            stateManager.getCurrentState().map.worldMap[int(self.posX)][int(self.posY)] = 0
        if self.startDeadAnim:
            if self.timePassed > self.deadAnimTime + self.stayDeadTime:
                self.startDeadAnim = False
                self.timePassed = 0
                stateManager.getCurrentState().map.sprites.remove(self)
            if self.timePassed > self.deadAnimTime:
                self.currentImage = self.deadSprites[len(self.deadSprites)-1]
            else:
                self.currentImage = self.deadSprites[int((self.timePassed * len(self.deadSprites))/self.deadAnimTime)]
            self.timePassed += delta
