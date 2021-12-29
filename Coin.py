import pygame
from OnBoard import OnBoard


class Coin(OnBoard):
    def __init__(self, raw_image, position):
        super(Coin, self).__init__(raw_image, position)
        self.__value = 5
        self.__coinAnimState = 0

    def updateImage(self, raw_image):
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (15, 15))

    def animateCoin(self):
        self.__coinAnimState = (self.__coinAnimState + 1) % 25
        if self.__coinAnimState / 5 == 0:
            self.updateImage(pygame.image.load('Image/coin1.png'))
        if self.__coinAnimState / 5 == 1:
            self.updateImage(pygame.image.load('Image/coin2.png'))
        if self.__coinAnimState / 5 == 2:
            self.updateImage(pygame.image.load('Image/coin3.png'))
        if self.__coinAnimState / 5 == 3:
            self.updateImage(pygame.image.load('Image/coin4.png'))
        if self.__coinAnimState / 5 == 4:
            self.updateImage(pygame.image.load('Image/coin5.png'))

    def collectCoin(self):
        return self.__value