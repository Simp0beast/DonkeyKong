import pygame


class OnBoard(pygame.sprite.Sprite):
    def __init__(self, raw_image, position):
        super(OnBoard, self).__init__()
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(self.image,
                                            (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def modifySize(self, raw_image, height, width):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (width, height))
