import pygame
import Settings
from Sprite import *
from GuardNpc import *
from ArmGuardNpc import *

class Map:
    worldMap = []
    sprites = []
    mapWidth = 100
    mapHeight = 64

    def __init__(self, mapName, player):
        self._image = pygame.image.load("Resources/Maps/"+mapName)
        self.sortedSprites=[]
        for y in range(self.mapHeight):
            self.worldMap.append([])
            for x in range(self.mapWidth):
                color = self._image.get_at((x, y))
                if(color.r == 255 and color.g == 255 and color.b == 255):
                    self.worldMap[y].append(0)
                elif(color.r == 255 and color.g == 0 and color.b == 255):
                    player.posX = y
                    player.posY = x
                    self.worldMap[y].append(80)
                elif(color.r == 0 and color.g == 0 and color.b == 0):
                    self.worldMap[y].append(2)
                elif(color.r == 64 and color.g == 64 and color.b == 64):
                    self.worldMap[y].append(4)
                elif(color.r == 90 and color.g == 0 and color.b == 0):
                    self.worldMap[y].append(1)
                elif(color.r == 180 and color.g == 0 and color.b == 0):
                    self.worldMap[y].append(7)
                elif(color.r == 0 and color.g == 0 and color.b == 255):
                    self.worldMap[y].append(5)
                elif(color.r == 128 and color.g == 128 and color.b == 128):
                    self.worldMap[y].append(8)
                elif(color.r == 0 and color.g == 255 and color.b == 0):
                    self.worldMap[y].append(12)
                elif(color.r == 150 and color.g ==255 and color.b ==150):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 12))
                elif(color.r == 0 and color.g ==128 and color.b ==0):
                    self.worldMap[y].append(14)
                elif(color.r == 255 and color.g ==150 and color.b ==0):
                    self.worldMap[y].append(15)
                elif(color.r == 0 and color.g ==0 and color.b ==150):
                    self.worldMap[y].append(16)
                elif(color.r == 0 and color.g ==64 and color.b ==0):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 16))
                elif(color.r == 255 and color.g ==64 and color.b ==0):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 17))
                elif(color.r == 0 and color.g ==0 and color.b ==64):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 18))
                elif(color.r == 255 and color.g ==255 and color.b ==0):
                    self.worldMap[y].append(6)
                elif(color.r == 114 and color.g ==0 and color.b ==0):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 8))
                elif(color.r == 50 and color.g ==50 and color.b ==50):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 9))
                elif(color.r == 255 and color.g ==200 and color.b ==200):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 10))
                elif(color.r == 0 and color.g ==130 and color.b ==110):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 19))
                elif(color.r == 0 and color.g ==255 and color.b ==200):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 20))
                elif(color.r == 240 and color.g ==230 and color.b ==250):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 21))
                elif(color.r == 250 and color.g ==110 and color.b ==0):
                    self.worldMap[y].append(90)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 22))
                elif(color.r == 255 and color.g ==180 and color.b ==255):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 23))
                elif(color.r == 0 and color.g ==0 and color.b ==70):
                    self.worldMap[y].append(0)
                    self.sprites.append(Sprite(y+0.5, x+0.5, 24))
                elif(color.r == 255 and color.g ==255 and color.b ==180):
                    self.worldMap[y].append(60)
                    self.sprites.append(GuardNpc(y+0.5, x+0.5, 60,Settings.DIFFICULTY))
                elif(color.r == 160 and color.g ==110 and color.b ==60):
                    self.worldMap[y].append(60)
                    self.sprites.append(ArmGuardNpc(y+0.5, x+0.5, 60,Settings.DIFFICULTY))
                elif(color.r == 176 and color.g ==255 and color.b ==20):
                    self.worldMap[y].append(26)
    def cleanUp(self):
        self.worldMap.clear()
        self.sprites.clear()
        self.sortedSprites.clear()
