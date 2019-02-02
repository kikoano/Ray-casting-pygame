import pygame
import FastCreate as fastCreate
from State import *
from Renderer import *
from Player import *
from Map import *
from EndState import *


class LevelState(State):

    initMouseY = False
    oldMouseX = 0
    walkableTiles = (0, 80)

    def init(self, stateManager):
        self.player = Player(0, 0, -1.0, 0.0, 0.0, 0.66)
        self.map = Map("level1.png", self.player)
        self.oldMapPos = (int(self.player.posX), int(self.player.posY))
        self.renderer = Renderer(stateManager.display, self.player, self.map)
        # Mouse for FPS
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        # Play music
        if Settings.MUSIC:
            pygame.mixer.music.load("Resources/Sounds/Music/turmoil.ogg")
            pygame.mixer.music.play(-1)

    def handleKeyEvents(self, stateManager):
        self.player.handleKeyEvents(stateManager)

    def update(self, delta, stateManager):
        # MOVE all this to player
        moveSpeed = self.player.moveSpeed * delta
        rotSpeed = self.player.rotSpeed * delta * abs(pygame.mouse.get_pos()[0]-self.oldMouseX)/Settings.MOUSE_SENSITIVITY

        # Move forward if no wall in front of you
        if self.player.move["forward"]:
            if self.map.worldMap[int(self.player.posX+self.player.dirX * moveSpeed)][int(self.player.posY)] in self.walkableTiles:
                self.player.posX += self.player.dirX * moveSpeed
            if self.map.worldMap[int(self.player.posX)][int(self.player.posY + self.player.dirY * moveSpeed)] in self.walkableTiles:
                self.player.posY += self.player.dirY * moveSpeed

        # Move backwards if no wall behind you
        if self.player.move["backward"]:
            if self.map.worldMap[int(self.player.posX - self.player.dirX * moveSpeed)][int(self.player.posY)]in self.walkableTiles:
                self.player.posX -= self.player.dirX * moveSpeed
            if self.map.worldMap[int(self.player.posX)][int(self.player.posY - self.player.dirY * moveSpeed)]in self.walkableTiles:
                self.player.posY -= self.player.dirY * moveSpeed

        # Strafe right if no wall in front of you
        if self.player.move["right"]:
            if self.map.worldMap[int(self.player.posX+self.player.planeX * moveSpeed)][int(self.player.posY)]in self.walkableTiles:
                self.player.posX += self.player.planeX * moveSpeed
            if self.map.worldMap[int(self.player.posX)][int(self.player.posY + self.player.planeY * moveSpeed)]in self.walkableTiles:
                self.player.posY += self.player.planeY * moveSpeed
        # Strafe left backwards if no wall behind you
        if self.player.move["left"]:
            if self.map.worldMap[int(self.player.posX - self.player.planeX * moveSpeed)][int(self.player.posY)]in self.walkableTiles:
                self.player.posX -= self.player.planeX * moveSpeed
            if self.map.worldMap[int(self.player.posX)][int(self.player.posY - self.player.planeY * moveSpeed)]in self.walkableTiles:
                self.player.posY -= self.player.planeY * moveSpeed

        # Rotate to the right
        if pygame.mouse.get_pos()[0] == 0:
            pygame.mouse.set_pos(stateManager.display.width/2, pygame.mouse.get_pos()[1])
        elif pygame.mouse.get_pos()[0] == stateManager.display.width-1:
            pygame.mouse.set_pos(stateManager.display.width/2, pygame.mouse.get_pos()[1])
        if pygame.mouse.get_pos()[0]-self.oldMouseX > 0:
            goRight = True
        else:
            goRight = False
        if self.player.move["rotateRight"] or(pygame.mouse.get_pos()[0] != self.oldMouseX and goRight):
            # Both camera direction and camera plane must be rotated
            if self.player.move["rotateRight"]:
                rotSpeed = self.player.rotSpeed * delta
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
        if self.player.move["rotateLeft"] or (pygame.mouse.get_pos()[0] != self.oldMouseX and not goRight):
            # Both camera direction and camera plane must be rotated
            if self.player.move["rotateLeft"]:
                rotSpeed = self.player.rotSpeed * delta
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
        # update map player pos
        self.map.worldMap[self.oldMapPos[0]][self.oldMapPos[1]] = 0
        self.map.worldMap[int(self.player.posX)][int(self.player.posY)] = 80
        self.oldMapPos = (int(self.player.posX), int(self.player.posY))

        if self.player.open:
            if self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 12 or self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 6:
                self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] = 0
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/door.wav"))
            elif self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 26:
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/door.wav"))
                stateManager.changeState(EndState(self.player))
            elif self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 14 and self.player.greenKey:
                self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] = 0
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/door.wav"))
            elif self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 15 and self.player.yellowKey:
                self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] = 0
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/door.wav"))
            elif self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] == 16 and self.player.blueKey:
                self.map.worldMap[int(self.player.posX+self.player.dirX)][int(self.player.posY+self.player.dirY)] = 0
                self.player.outside = False
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/door.wav"))
            self.player.open = False
        for sprite in self.map.sortedSprites:
            if(int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 12 and self.player.health < 100:
                self.player.health += 5
                self.player.healthPick += 1
                if self.player.health > 100:
                    self.player.health -= self.player.health % 100
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/pickup.wav"))
                self.map.sprites.remove(sprite)
            elif (int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 16:
                self.player.greenKey = True
                self.map.sprites.remove(sprite)
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/pickup.wav"))
            elif (int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 17:
                self.player.yellowKey = True
                self.map.sprites.remove(sprite)
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/pickup.wav"))
            elif (int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 18:
                self.player.blueKey = True
                self.map.sprites.remove(sprite)
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/pickup.wav"))
            elif (int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 23:
                self.player.pistolAmmo += 4
                self.player.ammoPick += 1
                self.map.sprites.remove(sprite)
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/ammo.wav"))
            elif (int(self.player.posX) == int(sprite.posX) and int(self.player.posY) == int(sprite.posY)) and sprite.texture == 24:
                self.player.weapons.append(Smg())
                self.player.currentWeapon = 1
                self.map.sprites.remove(sprite)
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound("Resources/Sounds/ammo.wav"))
            if sprite.texture >= 60:
                sprite.update(delta, stateManager)
        self.player.update(delta, stateManager, self.map)
        self.oldMouseX = pygame.mouse.get_pos()[0]

    def render(self, stateManager):
        self.renderer.render()
        self.player.render(stateManager)
        if not self.initMouseY:
            pygame.mouse.set_pos((stateManager.display.width/2, stateManager.display.height/2))
            self.initMouseY = True

    def cleanUp(self):
        self.map.cleanUp()
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
