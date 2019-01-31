import pygame


class Pistol:
    timePassed = 0
    animTime = 0.8
    currentImage = 0
    startAnim = False
    damage = 1

    sprites = [pygame.image.load("Resources/Weapons/pistol1.png"),
               pygame.image.load("Resources/Weapons/pistol2.png"),
               pygame.image.load("Resources/Weapons/pistol3.png"),
               pygame.image.load("Resources/Weapons/pistol4.png"),
               pygame.image.load("Resources/Weapons/pistol5.png")
               ]

    def update(self, delta):
        if self.startAnim:
            if self.timePassed > self.animTime:
                self.startAnim = False
                self.timePassed = 0
            self.currentImage = int((self.timePassed*len(self.sprites)) / self.animTime)
            self.timePassed += delta

    def render(self, stateManager):
        stateManager.display.surface.blit(pygame.transform.scale(
            self.sprites[self.currentImage], (64*6,  64*6)), (int((stateManager.display.width/2)-64*3), (stateManager.display.height-64*6)))

    def fire(self):
        self.startAnim = True
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/pistol.wav"))
