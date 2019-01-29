import math
from Entity import Entity
class Player(Entity):
    move ={
        "forward":False,
        "backward":False,
        "left":False,
        "right":False,
        "rotateLeft":False,
        "rotateRight":False
        }
    # Speed modifiers
    moveSpeed = 5.0
    rotSpeed = 3.0
    def __init__(self,posX,posY,dirX,dirY,planeX,planeY):
        super().__init__(posX,posY)
        self.planeX = planeX
        self.planeY = planeY
        self.dirX = dirX
        self.dirY = dirY
    def rotation(self):
        return math.degrees(math.atan2(self.dirY,self.dirX))