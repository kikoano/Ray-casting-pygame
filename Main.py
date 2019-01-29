import os
# Set the current working dir to the script path
# os.chdir(os.path.dirname(__file__))
import pygame
from Display import Display
from Renderer import Renderer
from Input import Input
from Player import Player
import time
# CONSTS
WIDTH = 640
HEIGH = 480
# TODO Player and Input class
# here should be the main loop


def main():
    pygame.init()
    display = Display(WIDTH, HEIGH)
    player = Player(22.0, 11.5, -1.0, 0.0, 0.0, 0.66)
    renderer = Renderer(display, player)

    lastTime = time.time()
    while True:
        # FPS counter
        deltaTime = time.time() - lastTime
        lastTime = time.time()
        Input.updateKeys(player)
        renderer.render(deltaTime)


if __name__ == "__main__":
    main()
