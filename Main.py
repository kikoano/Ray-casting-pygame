import pygame
from Display import *
from StateManager import *
from MenuState import *
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
    while True:
        # FPS counter
        deltaTime = time.time() - lastTime
        lastTime = time.time()
        stateManager.handleKeyEvents()
        stateManager.update(deltaTime)
        #TODO remove delta from render
        stateManager.render()

if __name__ == "__main__":
    main()
