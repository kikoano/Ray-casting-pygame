from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def handleKeyEvents(self,stateManager):
        pass

    @abstractmethod
    def update(self, delta,stateManager):
        pass

    @abstractmethod
    def render(self,stateManager):
        pass
    @abstractmethod
    def cleanUp(self):
        pass
