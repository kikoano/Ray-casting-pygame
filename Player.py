import math
import pygame
from pygame.locals import *
from Entity import Entity
import FastCreate as fastCreate
from Pistol import *
from Smg import *

class Player(Entity):
    move = {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
        "rotateLeft": False,
        "rotateRight": False,
    }
    grap = True

    open =False
    # Speed modifiers
    moveSpeed = 5.0
    rotSpeed = 3.0

    # Hp, Ammo and weapons
    health = 100
    pistolAmmo = 15
    selectedWeapon = 0
    weapons =[Pistol()]
    currentWeapon = 0
    fire=False

    #keys
    greenKey = False
    yellowKey = False
    blueKey = False

    outside=True
    bulletPassTiles = (0,90)

    hit = False
    currentTimeHit=0
    hitAnimTime=0.3

    kills = 0
    shots = 0
    aimShots = 0
    healthPick = 0
    ammoPick = 0

    alive = True

    def __init__(self, posX, posY, dirX, dirY, planeX, planeY):
        super().__init__(posX, posY)
        self.planeX = planeX
        self.planeY = planeY
        self.dirX = dirX
        self.dirY = dirY

    def rotation(self):
        return math.degrees(math.atan2(self.dirY, self.dirX))
    def update(self,delta,stateManager,map):
        if self.fire:
            self.weapons[self.currentWeapon].fire()
            self.fire=False
            self.rayCastFire(stateManager,map)
        self.weapons[self.currentWeapon].update(delta)
        if self.hit:
            if self.currentTimeHit > self.hitAnimTime:
                self.hit=False
                self.currentTimeHit=0
            self.currentTimeHit+=delta
        if not self.alive:
            import EndState as es
            stateManager.changeState(es.EndState(self))
    def handleKeyEvents(self, stateManager):
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                fastCreate.terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    self.move["forward"] = True
                elif event.key in (K_DOWN, K_s):
                    self.move["backward"] = True
                elif event.key in (K_LEFT, K_q):
                    self.move["rotateLeft"] = True
                elif event.key in (K_RIGHT, K_e):
                    self.move["rotateRight"] = True
                elif event.key == K_a:
                    self.move["left"] = True
                elif event.key == K_d:
                    self.move["right"] = True
                elif event.key == K_p:
                    if self.grap:
                        self.grap =False
                    else:
                        self.grap =True
                    pygame.event.set_grab(self.grap)
                    pygame.mouse.set_visible(not self.grap)
                elif event.key == K_f:
                    self.open=True
                elif event.key == K_ESCAPE:
                    import MenuState as ms
                    stateManager.changeState(ms.MenuState())
                elif event.key == K_SPACE:
                    self.gunUpdate()
                elif event.key == K_1:
                    self.currentWeapon=0
                elif event.key == K_2:
                    if len(self.weapons)>1:
                        self.currentWeapon=1

            elif event.type == KEYUP:
                if event.key in (K_UP, K_w):
                    self.move["forward"] = False
                elif event.key in (K_DOWN, K_s):
                    self.move["backward"] = False
                elif event.key in (K_LEFT, K_q):
                    self.move["rotateLeft"] = False
                elif event.key in (K_RIGHT, K_e):
                    self.move["rotateRight"] = False
                elif event.key == K_a:
                    self.move["left"] = False
                elif event.key == K_d:
                    self.move["right"] = False
                elif event.key == K_f:
                    self.open=False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.gunUpdate()
    def gunUpdate(self):
        if(self.pistolAmmo>0 and not self.weapons[self.currentWeapon].startAnim):
                    self.fire=True
                    self.pistolAmmo-=1
                    self.shots+=1
    def render(self,stateManager):
        self.weapons[self.currentWeapon].render(stateManager)
        if self.hit:
            screenDamage = pygame.Surface((stateManager.display.width, stateManager.display.height))
            screenDamage.set_alpha(30)
            screenDamage.fill(fastCreate.red)
            stateManager.display.surface.blit(screenDamage,(0,0))

    def takeDamage(self,damage):
        self.health-=damage
        if self.health <=0:
            self.alive =False
        self.hit=True

    def rayCastFire(self,stateManager,map):
        x = stateManager.display.width/2
        # calculate ray position and direction
        cameraX = 2.0 * x / stateManager.display.width - 1.0  # x-coordinate in camera space
        rayDirX = self.dirX + self.planeX * cameraX
        rayDirY = self.dirY + self.planeY * cameraX + .000000000000001  # avoiding ZDE
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
            if not map.worldMap[int(mapX)][int(mapY)] in self.bulletPassTiles:
                #find the npc
                for npc in map.sortedSprites:
                    if npc.texture == 60:
                        if int(npc.posX) == int(mapX) and int(npc.posY) == int(mapY):
                            npc.health-=self.weapons[self.currentWeapon].damage
                            self.aimShots+=1
                hit = 1