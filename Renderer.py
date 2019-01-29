import pygame
import math
from Texture import Texture
from Sprite import Sprite


class Renderer:
    mapWidth = 24
    mapHeight = 24
    texWidth = 64
    texHeight = 64
    worldMap = [
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 4, 6, 4, 4, 6, 4, 6, 4, 4, 4, 6, 4],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [8, 0, 3, 3, 0, 0, 0, 0, 0, 8, 8, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
        [8, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
        [8, 0, 3, 3, 0, 0, 0, 0, 0, 8, 8, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 4, 0, 0, 0, 0, 0, 6, 6, 6, 0, 6, 4, 6],
        [8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 4, 4, 6, 0, 0, 0, 0, 0, 6],
        [7, 7, 7, 7, 0, 7, 7, 7, 7, 0, 8, 0, 8, 0, 8, 0, 8, 4, 0, 4, 0, 6, 0, 6],
        [7, 7, 0, 0, 0, 0, 0, 0, 7, 8, 0, 8, 0, 8, 0, 8, 8, 6, 0, 0, 0, 0, 0, 6],
        [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 6, 0, 0, 0, 0, 0, 4],
        [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 6, 0, 6, 0, 6, 0, 6],
        [7, 7, 0, 0, 0, 0, 0, 0, 7, 8, 0, 8, 0, 8, 0, 8, 8, 6, 4, 6, 0, 6, 6, 6],
        [7, 7, 7, 7, 0, 7, 7, 7, 7, 8, 8, 4, 0, 6, 8, 4, 8, 3, 3, 3, 0, 3, 3, 3],
        [2, 2, 2, 2, 0, 2, 2, 2, 2, 4, 6, 4, 0, 0, 6, 0, 6, 3, 0, 0, 0, 0, 0, 3],
        [2, 2, 0, 0, 0, 0, 0, 2, 2, 4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 3],
        [2, 0, 0, 0, 0, 0, 0, 0, 2, 4, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 3],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 4, 4, 4, 6, 0, 6, 3, 3, 0, 0, 0, 3, 3],
        [2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 1, 2, 2, 2, 6, 6, 0, 0, 5, 0, 5, 0, 5],
        [2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 0, 5, 0, 5, 0, 0, 0, 5, 5],
        [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 5, 0, 5, 0, 5, 0, 5, 0, 5],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
        [2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 5, 0, 5, 0, 5, 0, 5, 0, 5],
        [2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 2, 2, 0, 5, 0, 5, 0, 0, 0, 5, 5],
        [2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    ]
    sprites = [
        Sprite(20.5, 11.5, 10),  # green light in front of playerstart
        # green lights in every room
        Sprite(18.5, 4.5, 10),
        Sprite(10.0, 4.5, 10),
        Sprite(10.0, 12.5, 10),
        Sprite(3.5, 6.5, 10),
        Sprite(3.5, 20.5, 10),
        Sprite(3.5, 14.5, 10),
        Sprite(14.5, 20.5, 10),
        # row of pillars in front of wall: fisheye test
        Sprite(18.5, 10.5, 9),
        Sprite(18.5, 11.5, 9),
        Sprite(18.5, 12.5, 9),

        # some barrels around the map
        Sprite(21.5, 1.5, 8),
        Sprite(15.5, 1.5, 8),
        Sprite(16.0, 1.8, 8),
        Sprite(16.2, 1.2, 8),
        Sprite(3.5,  2.5, 8),
        Sprite(9.5, 15.5, 8),
        Sprite(10.0, 15.1, 8),
        Sprite(10.5, 15.8, 8),
    ]
    ZBuffer = []
    spriteDistance = []

    # Textures
    texture = [Texture("eagle.png"), Texture("redbrick.png"), Texture("purplestone.png"), Texture(
        "greystone.png"), Texture("bluestone.png"), Texture("mossy.png"), Texture("wood.png"), Texture("colorstone.png"),
        Texture("barrel.png"), Texture("pillar.png"), Texture("greenlight.png")]
    # Skybox
    skybox = Texture("sky1.png")

    # Colors
    white = (255, 255, 255)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    black = (0, 0, 0)
    orange = (255, 100, 10)
    yellow = (255, 255, 0)
    blue_green = (0, 255, 170)
    marroon = (115, 0, 0)
    lime = (180, 255, 100)
    pink = (255, 100, 180)
    purple = (240, 0, 255)
    gray = (127, 127, 127)
    magenta = (255, 0, 230)
    brown = (100, 40, 0)
    forest_green = (0, 50, 0)
    navy_blue = (0, 0, 100)
    rust = (210, 150, 75)
    dandilion_yellow = (255, 200, 0)
    highlighter = (255, 255, 100)
    sky_blue = (0, 255, 255)
    light_gray = (200, 200, 200)
    dark_gray = (50, 50, 50)
    tan = (230, 220, 170)
    coffee_brown = (200, 190, 140)
    moon_glow = (235, 245, 255)

    def __init__(self, display, player):
        self.display = display
        self.player = player

    def _spriteDistance(self, sprite):
        return (sprite.posX - self.player.posX) ** 2 + (sprite.posY - self.player.posY) ** 2

    def render(self, delta):
        # Draws floor and celling

        averageColor = pygame.transform.average_color(self.display.surface)
        red = int(averageColor[0] / 30)*10+50
        green = int(averageColor[1] / 30)*10+50
        blue = int(averageColor[2] / 30)*10+50
        floorColor = (red, green, blue)
        self.display.surface.fill(floorColor)
        # fun code pygame.transform.average_color(self.display.surface) old was (25,25,25)
        #pygame.draw.rect(self.display.surface, (50, 50, 50),(0, self.display.height/2, self.display.width, self.display.height/2))
        left = self.player.rotation()-200
        if self.player.rotation() > 0.0:
            self.display.surface.blit(pygame.transform.scale(
                self.skybox.image, (self.display.width*2, int(self.display.height/2))), (left, 0))
        else:
            self.display.surface.blit(pygame.transform.scale(
                self.skybox.image, (self.display.width*2, int(self.display.height/2))), (left-230, 0))

        for x in range(self.display.width):
            # calculate ray position and direction
            cameraX = 2.0 * x / self.display.width - 1.0  # x-coordinate in camera space
            rayDirX = self.player.dirX + self.player.planeX * cameraX
            rayDirY = self.player.dirY + self.player.planeY * \
                cameraX + .000000000000001  # avoiding ZDE

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
                if self.worldMap[int(mapX)][int(mapY)] > 0:
                    hit = 1

            # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
            if side == 0:
                perpWallDist = (mapX - self.player.posX +
                                (1-stepX)/2) / rayDirX
            else:
                perpWallDist = (mapY - self.player.posY +
                                (1-stepY)/2) / rayDirY
            if perpWallDist == 0:
                perpWallDist = 0.000001

            # Calculate height of line to draw on screen
            lineHeight = int(self.display.height / perpWallDist)

            # Calculate lowest and highest pixel to fill in current stripe
            drawStart = -lineHeight / 2.0 + self.display.height / 2.0
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
            texNum = self.worldMap[mapX][mapY] - 1

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
            self.display.surface.blit(pygame.transform.scale(
                img[texX], (1, lineHeight)), (x, drawStart))

            # Set the ZBuffer for the sprite casting
            self.ZBuffer.append(perpWallDist)  # perpendicular distance is used

        # Sort sprites from far to close
        sortedSprites = sorted(self.sprites, key=self._spriteDistance)

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
            drawStartY = -spriteHeight / 2 + self.display.height / 2
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
                        self.display.surface.blit(pygame.transform.scale(self.texture[sprite.texture].converted[tex_x],(1, spriteHeight)),(stripe, drawStartY))
        # Clear ZBuffer
        self.ZBuffer.clear()
        moveSpeed = self.player.moveSpeed * delta
        rotSpeed = self.player.rotSpeed * delta

        # Move forward if no wall in front of you
        if self.player.move["forward"]:
            if not self.worldMap[int(self.player.posX+self.player.dirX * moveSpeed)][int(self.player.posY)]:
                self.player.posX += self.player.dirX * moveSpeed
            if not self.worldMap[int(self.player.posX)][int(self.player.posY + self.player.dirY * moveSpeed)]:
                self.player.posY += self.player.dirY * moveSpeed
        # Move backwards if no wall behind you
        if self.player.move["backward"]:
            if not self.worldMap[int(self.player.posX - self.player.dirX * moveSpeed)][int(self.player.posY)]:
                self.player.posX -= self.player.dirX * moveSpeed
            if not self.worldMap[int(self.player.posX)][int(self.player.posY - self.player.dirY * moveSpeed)]:
                self.player.posY -= self.player.dirY * moveSpeed

        # Strafe right if no wall in front of you
        if self.player.move["right"]:
            if not self.worldMap[int(self.player.posX+self.player.planeX * moveSpeed)][int(self.player.posY)]:
                self.player.posX += self.player.planeX * moveSpeed
            if not self.worldMap[int(self.player.posX)][int(self.player.posY + self.player.planeY * moveSpeed)]:
                self.player.posY += self.player.planeY * moveSpeed
        # Strafe left backwards if no wall behind you
        if self.player.move["left"]:
            if not self.worldMap[int(self.player.posX - self.player.planeX * moveSpeed)][int(self.player.posY)]:
                self.player.posX -= self.player.planeX * moveSpeed
            if not self.worldMap[int(self.player.posX)][int(self.player.posY - self.player.planeY * moveSpeed)]:
                self.player.posY -= self.player.planeY * moveSpeed

        # Rotate to the right
        if self.player.move["rotateRight"]:
            # Both camera direction and camera plane must be rotated
            oldDirX = self.player.dirX
            self.player.dirX = self.player.dirX * \
                math.cos(-rotSpeed) - self.player.dirY * math.sin(-rotSpeed)
            self.player.dirY = oldDirX * \
                math.sin(-rotSpeed) + self.player.dirY * math.cos(-rotSpeed)
            oldPlaneX = self.player.planeX
            self.player.planeX = self.player.planeX * \
                math.cos(-rotSpeed) - self.player.planeY * math.sin(-rotSpeed)
            self.player.planeY = oldPlaneX * \
                math.sin(-rotSpeed) + self.player.planeY * math.cos(-rotSpeed)
        # Rotate to the left
        if self.player.move["rotateLeft"]:
            # Both camera direction and camera plane must be rotated
            oldDirX = self.player.dirX
            self.player.dirX = self.player.dirX * \
                math.cos(rotSpeed) - self.player.dirY * math.sin(rotSpeed)
            self.player.dirY = oldDirX * \
                math.sin(rotSpeed) + self.player.dirY * math.cos(rotSpeed)
            oldPlaneX = self.player.planeX
            self.player.planeX = self.player.planeX * \
                math.cos(rotSpeed) - self.player.planeY * math.sin(rotSpeed)
            self.player.planeY = oldPlaneX * \
                math.sin(rotSpeed) + self.player.planeY * math.cos(rotSpeed)

        pygame.display.update()
