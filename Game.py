import pygame
import sys
from pygame.locals import *
from Board import Board


class Game:
    def __init__(self):
        self.height = 520
        self.width = 1200
        self.FPS = 30
        self.clock = pygame.time.Clock()
        self.displayScreen = pygame.display.set_mode((self.width, self.height))
        self.myFont = pygame.font.SysFont("comicsansms", 30)

        self.newGame = Board(self.width, self.height)

        self.barrelTimer = 0

        self.playerGroup = self.newGame.playerGroup
        self.wallGroup = self.newGame.wallGroup
        self.ladderGroup = self.newGame.ladderGroup

    def runGame(self):
        while 1:
            self.clock.tick(self.FPS)
            self.scoreLabel = self.myFont.render(str(self.newGame.score), 1,
                                                 (0, 0, 0))

            if self.newGame.gameState != 1:

                self.newGame.checkButton()
                self.newGame.redrawScreen(self.displayScreen, self.scoreLabel, self.width,
                                          self.height)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.newGame.processButton()
                        self.playerGroup = self.newGame.playerGroup
                        self.wallGroup = self.newGame.wallGroup
                        self.ladderGroup = self.newGame.ladderGroup

            if self.newGame.gameState == 1:

                self.barrelGroup = self.newGame.barrelGroup
                self.coinGroup = self.newGame.coinGroup

                if self.barrelTimer == 0:
                    self.newGame.CreateBarrel(self.newGame.Enemies[0].getPosition(), 0)
                elif len(self.newGame.Enemies) >= 2 and self.barrelTimer == 23:
                    self.newGame.CreateBarrel(self.newGame.Enemies[1].getPosition(), 1)
                elif len(self.newGame.Enemies) >= 3 and self.barrelTimer == 46:
                    self.newGame.CreateBarrel(self.newGame.Enemies[2].getPosition(), 2)
                self.barrelTimer = (self.barrelTimer + 1) % 70

                for coin in self.coinGroup:
                    coin.animateCoin()

                self.newGame.Players[0].updateY(2)
                self.laddersCollidedBelow = self.newGame.Players[0].checkCollision(self.ladderGroup)
                self.wallsCollidedBelow = self.newGame.Players[0].checkCollision(self.wallGroup)
                self.newGame.Players[0].updateY(-2)

                self.newGame.Players[0].updateY(-2)
                self.wallsCollidedAbove = self.newGame.Players[0].checkCollision(self.wallGroup)
                self.newGame.Players[0].updateY(2)

                self.newGame.ladderCheck(self.laddersCollidedBelow, self.wallsCollidedBelow, self.wallsCollidedAbove)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == KEYDOWN:
                        self.laddersCollidedExact = self.newGame.Players[0].checkCollision(self.ladderGroup)

                        if event.key == K_q:
                            self.newGame.gameState = 2
                            self.newGame.ActiveButtons[0] = 0
                            self.newGame.ActiveButtons[1] = 1
                            self.newGame.ActiveButtons[2] = 1

                        if (event.key == K_SPACE and self.newGame.Players[0].onLadder == 0) or (
                                event.key == K_w and self.laddersCollidedExact):
                            self.direction = 2
                            if self.newGame.Players[0].isJumping == 0 and self.wallsCollidedBelow:
                                self.newGame.Players[0].isJumping = 1
                                self.newGame.Players[0].currentJumpSpeed = 10

                self.newGame.Players[0].continuousUpdate(self.wallGroup, self.ladderGroup)

                keyState = pygame.key.get_pressed()
                if keyState[pygame.K_d]:
                    if self.newGame.direction != 4:
                        self.newGame.direction = 4
                        self.newGame.cycles = -1
                    self.newGame.cycles = (self.newGame.cycles + 1) % 10
                    if self.newGame.cycles < 5:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/right.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 15, 15)
                    else:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/right2.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 15, 15)
                    wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    if wallsCollidedExact:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/right.png'), "H",
                                                         -self.newGame.Players[0].getSpeed(), 15, 15)

                if keyState[pygame.K_a]:
                    if self.newGame.direction != 3:
                        self.newGame.direction = 3
                        self.newGame.cycles = -1
                    self.newGame.cycles = (self.newGame.cycles + 1) % 10
                    if self.newGame.cycles < 5:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/left.png'), "H",
                                                         -self.newGame.Players[0].getSpeed(), 15, 15)
                    else:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/left2.png'), "H",
                                                         -self.newGame.Players[0].getSpeed(), 15, 15)
                    wallsCollidedExact = self.newGame.Players[0].checkCollision(self.wallGroup)
                    if wallsCollidedExact:
                        self.newGame.Players[0].updateWH(pygame.image.load('Image/left.png'), "H",
                                                         self.newGame.Players[0].getSpeed(), 15, 15)

                if keyState[pygame.K_w] and self.newGame.Players[0].onLadder:
                    self.newGame.Players[0].updateWH(pygame.image.load('Image/still.png'), "V",
                                                     -self.newGame.Players[0].getSpeed() / 2, 15, 15)

                if keyState[pygame.K_s] and self.newGame.Players[0].onLadder:
                    self.newGame.Players[0].updateWH(pygame.image.load('Image/still.png'), "V",
                                                     self.newGame.Players[0].getSpeed() / 2, 15, 15)

                self.newGame.redrawScreen(self.displayScreen, self.scoreLabel, self.width, self.height)

                self.newGame.barrelCheck()

                coinsCollected = pygame.sprite.spritecollide(self.newGame.Players[0], self.coinGroup, True)
                self.newGame.coinCheck(coinsCollected)

                self.newGame.checkVictory(self.clock)

                for enemy in self.newGame.Enemies:
                    enemy.continuousUpdate(self.wallGroup, self.ladderGroup)

            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    createdGame = Game()
    createdGame.runGame()