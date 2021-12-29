import pygame
import math
import random
import sys

from Person import Person
from OnBoard import OnBoard
from Coin import Coin
from Player import Player
from Barrel import Barrel
from DonkeyKong import DonkeyKong
from Button import Button


class Board:
    def __init__(self, width, height):
        self.__width = width
        self.__actHeight = height
        self.__height = self.__actHeight + 10
        self.score = 0
        self.gameState = 0
        self.cycles = 0
        self.direction = 0

        self.white = (255, 255, 255)

        self.map = []
        self.Players = self.Enemies = self.Allies = self.Coins = self.Walls = self.Ladders = self.Barrels = self.Hearts = self.Boards = self.BarrelEndpoints = []

        self.resetGroups()

        self.Buttons = [Button(pygame.image.load('Image/start.png'), (500, 400), "start"),
                        Button(pygame.image.load('Image/exit.png'), (700, 400), "exit"),
                        Button(pygame.image.load('Image/restart.png'), (500, 400), "restart"), ]
        self.ActiveButtons = [1, 1, 0]
        self.myfont = pygame.font.SysFont("comicsansms", 50)

        self.background = pygame.image.load('Image/background.png')
        self.background = pygame.transform.scale(self.background, (width, height))
        self.startbackground = pygame.image.load('Image/buttonbackground.jpg')
        self.startbackground = pygame.transform.scale(self.startbackground, (width, height))
        self.barrelGroup = pygame.sprite.RenderPlain(self.Barrels)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.enemyGroup = pygame.sprite.RenderPlain(self.Enemies)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)
        self.barrelEndpointsGroup = pygame.sprite.RenderPlain(self.BarrelEndpoints)
        self.boardGroup = pygame.sprite.RenderPlain(self.Boards)
        self.heartGroup = pygame.sprite.RenderPlain(self.Hearts)

    def resetGroups(self):
        self.score = 0
        self.map = []
        self.Players = [Player(pygame.image.load('Image/still.png'), (50, 440))]
        self.Enemies = [DonkeyKong(pygame.image.load('Image/kong0.png'), (100, 117))]
        self.Allies = [Person(pygame.image.load('Image/princess.png'), (60, 55))]
        self.Allies[0].updateWH(self.Allies[0].image, "H", 0, 25, 25)
        self.Coins = []
        self.Walls = []
        self.Ladders = []
        self.Barrels = []
        self.Hearts = [OnBoard(pygame.image.load('Image/heart.png'), (730, 490)),
                       OnBoard(pygame.image.load('Image/heart.png'), (750, 490)),
                       OnBoard(pygame.image.load('Image/heart.png'), (770, 490))]
        self.Hearts[0].modifySize(pygame.image.load('Image/heart.png'), 20, 20)
        self.Hearts[1].modifySize(pygame.image.load('Image/heart.png'), 20, 20)
        self.Hearts[2].modifySize(pygame.image.load('Image/heart.png'), 20, 20)
        self.Boards = [OnBoard(pygame.image.load('Image/board.png'), (200, 480)),
                       OnBoard(pygame.image.load('Image/board.png'), (685, 480))]
        self.Boards[0].modifySize(self.Boards[0].image, 40, 150)
        self.Boards[1].modifySize(self.Boards[1].image, 40, 150)
        self.BarrelEndpoints = [OnBoard(pygame.image.load('Image/still.png'), (50, 440))]
        self.initializeGame()
        self.createGroups()
    def checkBarrelDestroy(self, barrel):
        if pygame.sprite.spritecollide(barrel, self.barrelEndpointsGroup, False):
            self.DestroyBarrel(barrel.index)


    def CreateBarrel(self, location, kongIndex):
        if len(self.Barrels) < len(self.Enemies) * 6+6:
            self.Barrels.append(
                Barrel(pygame.image.load('Image/2.png'), (location[0], location[1] + 15), len(self.Barrels),
                         2 + len(self.Enemies)/2))

            self.Enemies[kongIndex].setStopDuration(15)
            self.Enemies[kongIndex].setPosition(
                (self.Enemies[kongIndex].getPosition()[0], self.Enemies[kongIndex].getPosition()[1] - 12))
            self.Enemies[kongIndex].setCenter(self.Enemies[kongIndex].getPosition())
            self.createGroups()


    def DestroyBarrel(self, index):
        for barrel in range(len(self.Barrels)):
            if self.Barrels[barrel].index == index:
                self.Barrels.remove(self.Barrels[barrel])
                for barrelrem in range(
                        len(self.Barrels)):
                    if self.Barrels[barrelrem].index > index:
                        self.Barrels[barrelrem].index -= 1
                self.createGroups()
                break

    def GenerateCoins(self):
        for i in range(6, len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 0 and ((i + 1 < len(self.map) and self.map[i + 1][j] == 1) or (
                            i + 2 < len(self.map) and self.map[i + 2][j] == 1)):
                    randNumber = math.floor(random.random() * 1000)
                    if randNumber % 35 == 0 and len(self.Coins) <= 25:
                        self.map[i][j] = 3
                        if j - 1 >= 0 and self.map[i][j - 1] == 3:
                            self.map[i][j] = 0
                        if self.map[i][j] == 3:
                            self.Coins.append(Coin(pygame.image.load('Image/coin1.png'), (j * 15 + 15 / 2, i * 15 + 15 / 2)))
        if len(self.Coins) <= 20:
            self.GenerateCoins()

    def checkMapForMatch(self, placePosition, floor, checkNo, offset):
        if floor < 1:
            return 0
        for i in range(0, 5):
            if self.map[floor * 5 - offset][placePosition + i] == checkNo:
                return 1
            if self.map[floor * 5 - offset][placePosition - i] == checkNo:
                return 1
        return 0

    def makeMap(self):
        for point in range(0, self.__height // 15 + 1):
            row = []
            for point2 in range(0, self.__width // 15):
                row.append(0)
            self.map.append(row)

    def makeWalls(self):
        for i in range(0, (self.__height // 15) - 4):
            self.map[i][0] = self.map[i][self.__width // 15 - 1] = 1
        for i in range(0, (self.__height // (15 * 5))):
            for j in range(0, self.__width // 15):
                self.map[i * 5][j] = 1

    def makePrincessChamber(self):
        for j in range(0, 5):
            self.map[j][9] = 1
        for j in range(10, (self.__width // 15) - 1):
            self.map[1 * 5][j] = 0
        for j in range(0, 5):
            self.map[1 * 5 + j][7] = self.map[1 * 5 + j][8] = 2

    def makeLadders(self):
        for i in range(2, (self.__height // (15 * 5) - 1)):
            ladderPos = math.floor(random.random() * (self.__width // 15 - 20))
            ladderPos = int(10 + ladderPos)
            while self.checkMapForMatch(ladderPos, i - 1, 2, 0) == 1:
                ladderPos = math.floor(random.random() * (self.__width // 15 - 20))
                ladderPos = int(10 + ladderPos)
            for k in range(0, 5):
                self.map[i * 5 + k][ladderPos] = self.map[i * 5 + k][ladderPos + 1] = 2

    def makeHoles(self):
        for i in range(3, (self.__height // (15 * 5) - 1)):
            for k in range(1, 6):
                if i % 2 == 0:
                    self.map[i * 5][k] = 0
                else:
                    self.map[i * 5][self.__width // 15 - 1 - k] = 0

    def populateMap(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 1:
                    self.Walls.append(OnBoard(pygame.image.load('Image/wood_block.png'), (y * 15 + 15 // 2, x * 15 + 15 / 2)))
                elif self.map[x][y] == 2:
                    self.Ladders.append(OnBoard(pygame.image.load('Image/ladder.png'), (y * 15 + 15 // 2, x * 15 + 15 / 2)))

    def ladderCheck(self, laddersCollidedBelow, wallsCollidedBelow, wallsCollidedAbove):
        if laddersCollidedBelow and len(wallsCollidedBelow) == 0:
            for ladder in laddersCollidedBelow:
                if ladder.getPosition()[1] >= self.Players[0].getPosition()[1]:
                    self.Players[0].onLadder = 1
                    self.Players[0].isJumping = 0
                    if wallsCollidedAbove:
                        self.Players[0].updateY(3)
        else:
            self.Players[0].onLadder = 0

    def barrelCheck(self):
        for barrel in self.barrelGroup:
            barrel.continuousUpdate(self.wallGroup, self.ladderGroup)
            if barrel.checkCollision(self.playerGroup, "V"):
                if len(self.Hearts) >= 2:
                    self.Barrels.remove(barrel)
                    self.Hearts.pop(len(self.Hearts) - 1)
                    self.Players[0].setPosition((50, 440))
                    self.score -= 25
                    if self.score < 0:
                        self.score = 0
                    self.createGroups()
                else:
                    self.gameState = 2
                    self.ActiveButtons[0] = 0
                    self.ActiveButtons[1] = 1
                    self.ActiveButtons[2] = 1
            self.checkBarrelDestroy(barrel)

    def coinCheck(self, coinsCollected):
        for coin in coinsCollected:
            self.score += coin.collectCoin()
            self.map[int((coin.getPosition()[1] - 15 / 2) / 15)][int((coin.getPosition()[0] - 15 / 2) / 15)] = 0
            self.Coins.remove(coin)
            self.createGroups()

    def checkVictory(self, clock):
        if self.Players[0].checkCollision(self.allyGroup) or self.Players[0].getPosition()[1] < 5 * 15:

            clock.tick(100)
            self.score += 50

            self.Barrels = []
            self.Players[0].setPosition((50, 440))
            self.Coins = []
            self.GenerateCoins()

            if len(self.Enemies) == 1:
                self.Enemies.append(DonkeyKong(pygame.image.load('Image/kong0.png'), (700, 117)))
            elif len(self.Enemies) == 2:
                self.Enemies.append(DonkeyKong(pygame.image.load('Image/kong0.png'), (400, 117)))
            self.createGroups()

    def processButton(self):
        if self.ActiveButtons[0] == 1 and self.Buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            self.resetGroups()
            self.gameState = 1
            self.ActiveButtons[0] = 0
            self.ActiveButtons[1] = 0
            self.ActiveButtons[2] = 0
        if self.ActiveButtons[1] == 1 and self.Buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            pygame.quit()
            sys.exit()
        if self.ActiveButtons[2] == 1 and self.Buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
            self.gameState = 0
            self.ActiveButtons[0] = 1
            self.ActiveButtons[1] = 1
            self.ActiveButtons[2] = 0

    def checkButton(self):
        mousePosition = pygame.mouse.get_pos()
        for button in range(len(self.Buttons)):
            if self.ActiveButtons[button] == 1 and self.Buttons[button].rect.collidepoint(mousePosition):
                if button == 0:
                    self.Buttons[button].changeImage(pygame.image.load('Image/start1.png'))
                elif button == 1:
                    self.Buttons[button].changeImage(pygame.image.load('Image/exit1.png'))
                elif button == 2:
                    self.Buttons[button].changeImage(pygame.image.load('Image/restart1.png'))
            else:
                if button == 0:
                    self.Buttons[button].changeImage(pygame.image.load('Image/start.png'))
                elif button == 1:
                    self.Buttons[button].changeImage(pygame.image.load('Image/exit.png'))
                elif button == 2:
                    self.Buttons[button].changeImage(pygame.image.load('Image/restart.png'))

    def redrawScreen(self, displayScreen, scoreLabel, width, height):
        displayScreen.fill((0, 0, 0))
        if self.gameState != 1:
            displayScreen.blit(self.startbackground, self.startbackground.get_rect())
            if self.gameState == 2:
                label = self.myfont.render("Your score is " + str(self.score), 1, (255, 255, 255))
                displayScreen.blit(label, (410, 70))
            for button in range(len(self.ActiveButtons)):
                if self.ActiveButtons[button] == 1:
                    displayScreen.blit(self.Buttons[button].image, self.Buttons[button].getTopLeftPosition())
        if self.gameState == 1:
            displayScreen.blit(self.background, self.background.get_rect())
            self.ladderGroup.draw(displayScreen)
            self.playerGroup.draw(displayScreen)
            self.coinGroup.draw(displayScreen)
            self.wallGroup.draw(displayScreen)
            self.barrelGroup.draw(displayScreen)
            self.enemyGroup.draw(displayScreen)
            self.allyGroup.draw(displayScreen)
            self.boardGroup.draw(displayScreen)
            displayScreen.blit(scoreLabel, (265-scoreLabel.get_width()/2, 470))
            self.heartGroup.draw(displayScreen)

    def createGroups(self):
        self.barrelGroup = pygame.sprite.RenderPlain(self.Barrels)
        self.playerGroup = pygame.sprite.RenderPlain(self.Players)
        self.enemyGroup = pygame.sprite.RenderPlain(self.Enemies)
        self.wallGroup = pygame.sprite.RenderPlain(self.Walls)
        self.ladderGroup = pygame.sprite.RenderPlain(self.Ladders)
        self.coinGroup = pygame.sprite.RenderPlain(self.Coins)
        self.allyGroup = pygame.sprite.RenderPlain(self.Allies)
        self.barrelEndpointsGroup = pygame.sprite.RenderPlain(self.BarrelEndpoints)
        self.boardGroup = pygame.sprite.RenderPlain(self.Boards)
        self.heartGroup = pygame.sprite.RenderPlain(self.Hearts)


    def initializeGame(self):
        self.makeMap()
        self.makeWalls()
        self.makePrincessChamber()
        self.makeLadders()
        self.makeHoles()
        self.GenerateCoins()
        self.populateMap()
        self.createGroups()