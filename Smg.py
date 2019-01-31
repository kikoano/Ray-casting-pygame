import pygame


class Smg:
    timePassed = 0
    animTime = 0.6
    currentImage = 0
    startAnim = False
    damage = 2
    sprites = [pygame.image.load("Resources/Weapons/smg1.png"),
               pygame.image.load("Resources/Weapons/smg2.png"),
               pygame.image.load("Resources/Weapons/smg3.png"),
               pygame.image.load("Resources/Weapons/smg4.png"),
               pygame.image.load("Resources/Weapons/smg5.png")
               ]
    def update(self, delta):
        if self.startAnim:
            if(self.timePassed > self.animTime):
                self.startAnim = False
                self.timePassed = 0
            self.currentImage = int((self.timePassed*len(self.sprites)) / self.animTime)
            self.timePassed += delta

    def render(self, stateManager):
        stateManager.display.surface.blit(pygame.transform.scale(
            self.sprites[self.currentImage], (64*6,  64*6)), (int((stateManager.display.width/2)-64*3), (stateManager.display.height-64*6)))

    def fire(self):
        self.startAnim = True
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/smg.wav"))
