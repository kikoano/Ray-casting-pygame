from Entity import Entity

class Sprite(Entity):
    def __init__(self, posX, posY, texture,block=False):
        super().__init__(posX, posY)
        self.texture = texture
        self.block = block
