from Sprite import *
from Texture import *
import random
import pygame

class ArmGuardNpc(Sprite):
    health = 4
    damage = 8
    idleSprite = Texture("armGuardIdle.bmp", True)
    currentImage = idleSprite

    deadSprites = [
        Texture("armGuardDead1.bmp", True),
        Texture("armGuardDead2.bmp", True),
        Texture("armGuardDead3.bmp", True),
        Texture("armGuardDead4.bmp", True),
        Texture("armGuardDead5.bmp", True)
    ]
    shootSprites = [
        Texture("armGuardShoot1.bmp", True),
        Texture("armGuardShoot2.bmp", True),
        Texture("armGuardShoot3.bmp", True)
    ]
    moveSprites = [
        Texture("armGuardMove1.bmp", True),
        Texture("armGuardMove2.bmp", True),
        Texture("armGuardMove3.bmp", True),
        Texture("armGuardMove4.bmp", True)
    ]
    timePassed = 0
    stayDeadTime = 10
    deadAnimTime = 1
    startDeadAnim = False

    tryShootTime = 1.0
    tryShootPassedTime = 0

    shootAnimTime = 0.5
    startShootAnim = False
    timePassedShoot = 0

    moveAnimTime = 0.8
    timePassedMove = 0

    alive = True
    stop = False
    moveSpeed = 0.4
    moveableTiles = (0,60)


    def __init__(self, posX, posY, texture,dif ,block=False):
        super().__init__(posX, posY, texture, block)
        self.oldMapPos = (int(self.posX), int(self.posY))
        self.damage+=dif

    def update(self, delta, stateManager):
        # check if dead and do death animation
        if self.health <= 0 and not self.startDeadAnim:
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/enemyDeath2.wav"))
            self.startDeadAnim = True
            self.alive = False
            stateManager.getCurrentState().player.kills+=1
            stateManager.getCurrentState().map.worldMap[int(self.posX)][int(self.posY)] = 0
        self.shootAnim(delta,stateManager)
        self.deadAnim(delta,stateManager)
        # shoot if alive and see Player
        if self.seePlayer(stateManager) and self.alive:
            if not self.startShootAnim:
                self.move(delta,stateManager)
            self.shootChance(delta, stateManager)
    #Dead animation
    def deadAnim(self, delta, stateManager):
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
    # Shoot animation
    def shootAnim(self,delta,stateManager):
        if self.startShootAnim:
            if self.timePassedShoot > self.shootAnimTime:
                self.startShootAnim = False
                self.timePassedShoot = 0
                self.currentImage =  self.idleSprite
            else:
                self.currentImage = self.shootSprites[int((self.timePassedShoot * len(self.shootSprites))/self.shootAnimTime)]
            self.timePassedShoot += delta
    # Move animation
    def moveAnim(self,delta,stateManager):
        if self.timePassedMove > self.moveAnimTime:
            self.timePassedMove = 0
        self.currentImage = self.moveSprites[int((self.timePassedMove * len(self.moveSprites))/self.moveAnimTime)]
        self.timePassedMove += delta
    def shootChance(self, delta, stateManager):
        if self.tryShootPassedTime > self.tryShootTime:
            self.tryShootPassedTime = 0
            self.startShootAnim = True
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/enemyFire2.wav"))
            # miss fire
            miss = random.random()
            if miss > 0.2:
                stateManager.getCurrentState().player.takeDamage(self.damage) 
        else:
            self.tryShootPassedTime += delta
    def move(self,delta,stateManager):
        #calcualte distance
        distance = (self.posX - stateManager.getCurrentState().player.posX) ** 2 + (self.posY - stateManager.getCurrentState().player.posY) ** 2
        if distance < 3:
            self.currentImage = self.idleSprite
            return
        self.moveAnim(delta,stateManager)
        moveSpeed = self.moveSpeed * delta
        x = stateManager.display.width/2
        # calculate ray position and direction
        cameraX = 2.0 * x / stateManager.display.width - 1.0  # x-coordinate in camera space
        rayDirX = stateManager.getCurrentState().player.posX - self.posX + stateManager.getCurrentState().player.planeX * cameraX
        rayDirY = stateManager.getCurrentState().player.posY - self.posY + stateManager.getCurrentState().player.planeY * cameraX + .000000000000001  # avoiding ZDE
        if stateManager.getCurrentState().map.worldMap[int(self.posX+rayDirX * moveSpeed)][int(self.posY)] in self.moveableTiles:
                self.posX += rayDirX * moveSpeed
        if stateManager.getCurrentState().map.worldMap[int(self.posX)][int(self.posY + rayDirY * moveSpeed)] in self.moveableTiles:
                self.posY += rayDirY * moveSpeed
        
        # update map NPC pos
        stateManager.getCurrentState().map.worldMap[self.oldMapPos[0]][self.oldMapPos[1]] = 0
        stateManager.getCurrentState().map.worldMap[int(self.posX)][int(self.posY)] = 60
        self.oldMapPos = (int(self.posX), int(self.posY))

    def seePlayer(self,stateManager):
        see = False
        x = stateManager.display.width/2
        # calculate ray position and direction
        cameraX = 2.0 * x / stateManager.display.width - 1.0  # x-coordinate in camera space
        rayDirX = stateManager.getCurrentState().player.posX - self.posX + stateManager.getCurrentState().player.planeX * cameraX
        rayDirY = stateManager.getCurrentState().player.posY - self.posY + stateManager.getCurrentState().player.planeY * cameraX + .000000000000001  # avoiding ZDE
        # which box of the map we are in
        mapX = int(self.posX)
        mapY = int(self.posY)
        # lenght of ray from current position to next x or y-side
        sideDistX = None
        sideDistY = None
        # lenght of ray from one x or y-side to next x or y-side
        deltaDistX = abs(1.0/rayDirX)
        deltaDistY = abs(1.0/rayDirY)
        # what direction to step in x or y-direction (either +1 or -1)
        stepX = None
        stepY = None
        hit = 0  # was there a wall hit?
        side = None  # was a NS or EW wall hit?
        # calculate step and initial sideDist
        if rayDirX < 0:
            stepX = -1
            sideDistX = (self.posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1 - self.posX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (self.posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1 - self.posY) * deltaDistY
        # perform DDA
        while hit == 0:
            # jump to next map square, OR in x-direction, OR in y-direction
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            # check if ray has hit a wall
            #print(str(int(mapX))+" "+str(int(mapY)))
            tile = stateManager.getCurrentState().map.worldMap[int(mapX)][int(mapY)]
            if not tile in stateManager.getCurrentState().player.bulletPassTiles:
                if tile == 80:
                    return True
                return False
                hit = 1