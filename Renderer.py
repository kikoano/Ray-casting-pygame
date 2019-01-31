import pygame
import math
from Texture import *
from Sprite import *
import FastCreate as fastCreate
from GuardNpc import *

class Renderer:
    texWidth = 64
    texHeight = 64

    ZBuffer = []
    spriteDistance = []

    # Textures
    texture = [Texture("eagle.png"), Texture("redbrick.png"), Texture("purplestone.png"), Texture(
        "greystone.png"), Texture("bluestone.png"), Texture("mossy.png"), Texture("wood.png"), Texture("colorstone.png"),
        Texture("barrel.png"), Texture("pillar.png"), Texture("greenlight.png"),Texture("door.png"),Texture("health.png"),Texture("greenDoor.png"),
        Texture("yellowDoor.png"),Texture("blueDoor.png"),Texture("greenKey.png"),Texture("yellowKey.png"),Texture("blueKey.png"),Texture("greenBarrel.bmp"),Texture("tree.bmp"),
        Texture("bed.bmp"),Texture("table.bmp"),Texture("ammo.png"),Texture("smg.png")]
    # Skybox
    skybox = Texture("sky1.png")

    oldMouseX=0
    centered = False
    def __init__(self, display, player,map):
        self.display = display
        self.player = player
        self.map = map

    def _spriteDistance(self, sprite):
        return (sprite.posX - self.player.posX) ** 2 + (sprite.posY - self.player.posY) ** 2
    def renderHud(self):
        # Health bar
        healthBar = pygame.Surface((self.player.health*1.5,24))
        healthBarText= fastCreate.makeText("Health: "+str(self.player.health)+"%",self.display.fontHud,fastCreate.black,22,self.display.height-38)
        healthBar.set_alpha(200)
        healthBar.fill(fastCreate.green)
        
        # Health bar outline
        healthBarOut = pygame.Surface((100*1.5+4,25+4),pygame.SRCALPHA)
        healthBarOut.set_alpha(200)
        pygame.draw.rect(healthBarOut,fastCreate.black,healthBarOut.get_rect(),4)

        # Health bar back
        healthBarBack = pygame.Surface((100*1.5,24))
        healthBarBack.set_alpha(200)
        healthBarBack.fill(fastCreate.gray)

        self.display.surface.blit(healthBarOut,(18,self.display.height-42))
        self.display.surface.blit(healthBarBack,(20,self.display.height-39))
        self.display.surface.blit(healthBar,(20,self.display.height-39))
        self.display.surface.blit(healthBarText[0],healthBarText[1])
        # Keys
        keySlotBack = pygame.Surface((124,40))
        keySlotBack.set_alpha(200)
        keySlotBack.fill(fastCreate.gray)
        self.display.surface.blit(keySlotBack,(self.display.width/2+60,self.display.height-42))
        
        for i in range(3):
            keySlot = pygame.Surface((40+4,40+4),pygame.SRCALPHA)
            pygame.draw.rect(keySlot,fastCreate.black,keySlot.get_rect(),5)
            self.display.surface.blit(keySlot,(self.display.width/2-(i*42)+142,self.display.height-44))
        if self.player.greenKey:
            self.display.surface.blit(pygame.image.load("Resources/Textures/greenKeyIcon.png"),(self.display.width/2+64,self.display.height-30))
        if self.player.yellowKey:
            self.display.surface.blit(pygame.image.load("Resources/Textures/yellowKeyIcon.png"),(self.display.width/2+106,self.display.height-30))
        if self.player.blueKey:
            self.display.surface.blit(pygame.image.load("Resources/Textures/blueKeyIcon.png"),(self.display.width/2+148,self.display.height-30))
        # Ammo
        ammoBack = pygame.Surface((115,25))
        ammoBack.set_alpha(200)
        ammoBack.fill(fastCreate.gray)
        self.display.surface.blit(ammoBack,(self.display.width-128,self.display.height-41))
        ammoText= fastCreate.makeText("Ammo: "+str(self.player.pistolAmmo),self.display.fontHud,fastCreate.black,self.display.width-120,self.display.height-38)
        self.display.surface.blit(ammoText[0],ammoText[1]) 
    def render(self):
        # Draws floor and celling
        averageColor = pygame.transform.average_color(self.display.surface)
        red = int(averageColor[0] / 50)*10+50
        green = int(averageColor[1] / 50)*10+50
        blue = int(averageColor[2] / 50)*10+50
        floorColor = (red, green, blue)
        if self.player.outside:
            left = self.player.rotation()-self.display.width/2
            if self.player.rotation() > 0.0:
                self.display.surface.blit(pygame.transform.scale(
                    self.skybox.image, (self.display.width*2, self.display.height)), (left, 0))
            else:
                self.display.surface.blit(pygame.transform.scale(
                    self.skybox.image, (self.display.width*2, self.display.height)), (left+self.display.width/2, 0))

            floor = pygame.Surface((self.display.width,self.display.height/2+(pygame.mouse.get_pos()[1]*4) +self.display.height*2))

            floor.fill(floorColor)

            self.display.surface.blit(floor,(0,self.display.height/2-(pygame.mouse.get_pos()[1]*4) +self.display.height*2))
        else:
             self.display.surface.fill(floorColor)

        for x in range(self.display.width):
            # calculate ray position and direction
            cameraX = 2.0 * x / self.display.width - 1.0  # x-coordinate in camera space
            rayDirX = self.player.dirX + self.player.planeX * cameraX
            rayDirY = self.player.dirY + self.player.planeY * cameraX + .000000000000001  # avoiding ZDE

            # which box of the map we are in
            mapX = int(self.player.posX)
            mapY = int(self.player.posY)

            # lenght of ray from current position to next x or y-side
            sideDistX = None
            sideDistY = None

            # lenght of ray from one x or y-side to next x or y-side
            deltaDistX = abs(1.0/rayDirX)
            deltaDistY = abs(1.0/rayDirY)
            perpWallDist = None

            # what direction to step in x or y-direction (either +1 or -1)
            stepX = None
            stepY = None

            hit = 0  # was there a wall hit?
            side = None  # was a NS or EW wall hit?

            # calculate step and initial sideDist
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.player.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1 - self.player.posX) * deltaDistX
            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.player.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1 - self.player.posY) * deltaDistY

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
                if self.map.worldMap[int(mapX)][int(mapY)] > 0 and self.map.worldMap[int(mapX)][int(mapY)] < 60:
                    hit = 1

            # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
            if side == 0:
                perpWallDist = (mapX - self.player.posX +(1-stepX)/2) / rayDirX
            else:
                perpWallDist = (mapY - self.player.posY +(1-stepY)/2) / rayDirY
            if perpWallDist == 0:
                perpWallDist = 0.000001

            # Calculate height of line to draw on screen
            lineHeight = int(self.display.height / perpWallDist)

            # Calculate lowest and highest pixel to fill in current stripe
            drawStart = -lineHeight / 2.0 + self.display.height / 2.0 -(pygame.mouse.get_pos()[1]*4) +self.display.height*2
            
            # if drawStart < 0:
            #    drawStart = 0
            #drawEnd = lineHeight / 2 + self.display.height / 2.0
            # if drawEnd >= self.display.height:
            #    drawEnd = self.display.height-1
            if lineHeight > 10000:
                lineHeight = 10000
                drawStart = -10000 / 2 + self.display.height/2

            # Texturing calculations
            # 1 subtracted from it so that texture 0 can be used!
            texNum = self.map.worldMap[mapX][mapY] - 1

            # Calculate value of wallX
            wallX = None  # Where exactly the wall was hit
            if side == 0:
                wallX = self.player.posY + perpWallDist * rayDirY
            else:
                wallX = self.player.posX + perpWallDist * rayDirX
            wallX -= math.floor(wallX)

            # x coordinate on the texture
            texX = int(wallX * float(self.texWidth))
            if side == 0 and rayDirX > 0:
                texX = self.texWidth - texX - 1
            if side == 1 and rayDirY < 0:
                texX = self.texWidth - texX - 1

            # for y in range(int(drawStart),int(drawEnd)):
                # d = y * 256 - self.display.height * 128 + lineHeight * 128 # 256 and 128 factors to aboid floats
                # TODO avoid the division to speed this up
                #texY = ((d*self.texHeight) / lineHeight) / 256
                #color = self.texture[texNum].buffer[int(self.texHeight * texY + texX)]
                # Make color darker for y-sides: R, G and B byte each divided through two with a "shift" and an "and"
                # if side == 1:
                #    color = (color >> 1) & 8355711
            img = self.texture[texNum].converted if side == 0 else self.texture[texNum].converted_darkened
            self.display.surface.blit(pygame.transform.scale(img[texX], (1, lineHeight)), (x, drawStart))

            # Set the ZBuffer for the sprite casting
            self.ZBuffer.append(perpWallDist)  # perpendicular distance is used

        # Sort sprites from far to close
        sortedSprites = sorted(self.map.sprites, key=self._spriteDistance)

        # After sorting the sprites, do the projection and draw them
        for sprite in reversed(sortedSprites):
            # Translate sprite position to relative to camera
            # The 0.5 * something part servers to push the Sprite half a tile back
            spriteX = sprite.posX - self.player.posX 
            spriteY = sprite.posY - self.player.posY 
            # Transform sprite with the inverse camera matrix
            # [ planeX   dirX ] -1                                       [ dirY      -dirX ]
            # [               ]       =  1/(planeX*dirY-dirX*planeY) *   [                 ]
            # [ planeY   dirY ]                                          [ -planeY  planeX ]
            # required for corect matrix multiplication
            invDet = 1.0 / (self.player.planeX * self.player.dirY - self.player.dirX * self.player.planeY)
            transformX = invDet * (self.player.dirY * spriteX - self.player.dirX * spriteY)
            # This is actually the depth inside the screen, that what Z is in 3D
            transformY = invDet * (self.player.planeX * spriteY - self.player.planeY * spriteX)
            if transformY < 0:
                continue  # The sprite is not even in front of the camera, go to next one
            # Calculate where on the screen to start drawing the sprite and where to end
            spriteSurfaceX = int((self.display.width / 2) * (1 + transformX / transformY))
            # Calculate height of the sprite on screen
            spriteHeight = abs(int(self.display.height / (transformY)))  # Using "transformY" instead of the real distance prevents fisheye
            # Calculate width of the sprite
            spriteWidth = abs(int(self.display.height / (transformY)))
            drawStartY = -spriteHeight / 2 + self.display.height / 2 -(pygame.mouse.get_pos()[1]*4) +self.display.height*2
            drawEndY = spriteHeight / 2 + self.display.height / 2
            drawStartX = -spriteWidth / 2 + spriteSurfaceX
            drawEndX = spriteWidth / 2 + spriteSurfaceX
            if spriteHeight < 1000:
                for stripe in range(int(drawStartX), int(drawEndX)):
                    if (
                        stripe >= 0 and stripe < self.display.width and  # is the stripe even within screen boundaries?
                        transformY < self.ZBuffer[stripe]  # isn't this stripe obscured by a wall?
                    ):
                        # Find out which column of pixels to grab from the pixel-table turned image.
                        tex_x = int((stripe - (-spriteWidth / 2 + spriteSurfaceX)) * 64 / spriteWidth)
                        # Finally blit a column of pixels.
                        if isinstance(sprite,GuardNpc) :
                            tex = sprite.currentImage.converted[tex_x]
                        else:
                            tex =self.texture[sprite.texture].converted[tex_x]
                        self.display.surface.blit(pygame.transform.scale(tex,(1, spriteHeight)),(stripe, drawStartY))
        # Clear ZBuffer
        self.ZBuffer.clear()
        
        self.renderHud()
