import pygame
import sys
from pygame.locals import *

class Input:
    @staticmethod
    def updateKeys(player):
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                Input.terminate()

            elif event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    player.move["forward"] = True
                elif event.key in (K_DOWN, K_s):
                    player.move["backward"] = True
                elif event.key in (K_LEFT, K_a):
                    player.move["rotateLeft"] = True
                elif event.key in (K_RIGHT, K_d):
                    player.move["rotateRight"] = True
                elif event.key == K_q:
                    player.move["left"] = True
                elif event.key == K_e:
                    player.move["right"] = True

            elif event.type == KEYUP:
                if event.key in (K_UP, K_w):
                    player.move["forward"] = False
                elif event.key in (K_DOWN, K_s):
                    player.move["backward"] = False
                elif event.key in (K_LEFT, K_a):
                    player.move["rotateLeft"] = False
                elif event.key in (K_RIGHT, K_d):
                    player.move["rotateRight"] = False
                elif event.key == K_q:
                    player.move["left"] = False
                elif event.key == K_e:
                    player.move["right"] = False
                elif event.key == K_ESCAPE:
                    Input.terminate()

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()
