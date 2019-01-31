import pygame
from Renderer import *
from Player import *


class StateManager:
    __states = []

    def __init__(self, display):
        self.display = display

    def changeState(self, state):
        if len(self.__states) > 0:
            self.__states[-1].cleanUp()
            self.__states.pop()
        self.__states.append(state)
        self.__states[-1].init(self)

    def pushState(self, state):
        self.__states.append(state)
        self.__states[-1].init(self)

    def popState(self):
        if len(self.__states) > 0:
            self.__states[-1].cleanUp()
            self.__states.pop()

    def handleKeyEvents(self):
        self.__states[-1].handleKeyEvents(self)

    def update(self, delta):
        self.__states[-1].update(delta, self)

    def render(self):
        self.__states[-1].render(self)
        
    def getCurrentState(self):
        return self.__states[-1]
