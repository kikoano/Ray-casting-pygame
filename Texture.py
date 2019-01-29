import pygame

class Texture:

    def __init__(self,path):
        self._image = pygame.image.load("Resources/Textures/"+path)
        self._converted = None
        self._converted_darkened = None

    @property
    def image(self):
        return self._image

    @property
    def converted(self):
        if self._converted is None:
            self._converted = self.__convert_to_pixel_table()
            self._converted_darkened = self.__convert_to_pixel_table(True)
        return self._converted

    @property
    def converted_darkened(self):
        if self._converted is None:
            self._converted = self.__convert_to_pixel_table()
            self._converted_darkened = self.__convert_to_pixel_table(True)
        return self._converted_darkened

    def __convert_to_pixel_table(self, darken=False):
        image = self._image
        table = []
        if darken:
            image.set_alpha(192)
        for i in range(image.get_width()):
            s = pygame.Surface((1, image.get_height())).convert()
            s.blit(image, (-i, 0))
            s.set_colorkey((0,0,0)) ## this means full black color is now transparent
            table.append(s)
        return table
