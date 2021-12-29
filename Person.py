import pygame


class Person(pygame.sprite.Sprite):
    def __init__(self, raw_image, position):
        super(Person, self).__init__()
        self.__position = position
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = self.__position

    def getSpeed(self):
        raise NotImplementedError()

    def setCenter(self, position):
        self.rect.center = position

    def getPosition(self):
        return self.__position

    def setPosition(self, position):
        self.__position = position

    def updateWH(self, raw_image, direction, value, height, width):
        if direction == "H":
            self.__position = (self.__position[0] + value, self.__position[1])
        if direction == "V":
            self.__position = (self.__position[0], self.__position[1] + value)
        self.image = raw_image
        self.image = pygame.transform.scale(self.image, (height, width))
        self.rect.center = self.__position

    def updateY(self, value):
        self.__position = (self.__position[0], self.__position[1] + value)
        self.rect.center = self.__position

    def checkCollision(self, colliderGroup):
        Colliders = pygame.sprite.spritecollide(self, colliderGroup, False)
        return Colliders

    def continuousUpdate(self, GroupList,GroupList2):
        raise NotImplementedError()
