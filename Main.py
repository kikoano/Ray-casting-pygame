import pygame
from Display import *
from StateManager import *
from MenuState import *
import FastCreate as fastCreate
import time
# CONSTS
WIDTH = 640
HEIGH = 480

def main():
    pygame.init()
    pygame.mixer.init()
    display = Display(WIDTH, HEIGH)
    stateManager = StateManager(display)
    stateManager.pushState(MenuState())

    lastTime = time.time()
    frameTimes = [1]
    while True:
        # FPS counter
        deltaTime = time.time() - lastTime
        lastTime = time.time()
        frameTimes.append(deltaTime)
        frameTimes = frameTimes[-20:]
        fps = len(frameTimes) / sum(frameTimes)
        textFps = fastCreate.makeText(str(int(fps)),display.font,(0,255,0),0,0)

        stateManager.handleKeyEvents()
        stateManager.update(deltaTime)
        stateManager.render()
        display.surface.blit(textFps[0],textFps[1])
        pygame.display.update()
if __name__ == "__main__":
    main()
