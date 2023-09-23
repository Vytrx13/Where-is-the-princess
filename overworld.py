import pygame
from game_data import *
from tile import *

class Overworld:
    def __init__(self, startLevel,maxLevel,surface, collectedCoins):
        
        #setup 
        self.displaySurface = surface
        self.maxLevel = maxLevel
        self.currentLevel = startLevel
        self.collectedCoins = collectedCoins
        
        # sprites
        self.setupNodes()
        self.setupArrow()
        self.setupCoins()
        
        self.text = pygame.sprite.GroupSingle()
        text = Text("Use the arrow keys to select a level and the space bar to confirm", (500, SCREEN_HEIGHT-50), 30, 'purple')
        self.text.add(text)
        
    def setupNodes(self):
        self.nodes = pygame.sprite.Group()
        for i,node_data in enumerate(levels.values()):
            if i <= self.maxLevel:
                nodeSprite = Node(node_data['pos'], 'available', i)
                
            else:
                nodeSprite = Node(node_data['pos'], 'locked', i)
            
            self.nodes.add(nodeSprite)
            
    def setupArrow(self):
        self.arrow = pygame.sprite.GroupSingle()
        arrowSprite = Arrow(self.nodes.sprites()[self.currentLevel].rect.center)
        self.arrow.add(arrowSprite)
        
    def setupCoins(self):
        self.coins = pygame.sprite.Group()
        for num in range(6):
            coin = Coin((110 + num*100, 350), self.collectedCoins[num])
            self.coins.add(coin)
                
                
        
        
    # def input(self):
    #     keys = pygame.key.keys_get_pressed()
        
    #     if keys[pygame.K_RIGHT] and self.currentLevel < self.maxLevel:
    #         self.currentLevel += 1
    #         self.arrow.remove(self.arrow.sprite)
    #         self.setupArrow()
                
    #     elif keys[pygame.K_LEFT] and self.currentLevel > 0:
    #         self.currentLevel -= 1
    #         self.arrow.remove(self.arrow.sprite)
    #         self.setupArrow()
    
    def moveArrow(self, direction):
        if direction == "right" and self.currentLevel < self.maxLevel :
            self.currentLevel += 1
            self.arrow.remove(self.arrow.sprite)
            self.setupArrow()
        elif direction == "left" and self.currentLevel > 0:
            self.currentLevel -= 1
            self.arrow.remove(self.arrow.sprite)
            self.setupArrow()
            
            
    def run(self):
        self.nodes.draw(self.displaySurface)
        self.arrow.draw(self.displaySurface)
        self.coins.draw(self.displaySurface)
        self.text.draw(self.displaySurface)
    
    
class Node(pygame.sprite.Sprite):
    def __init__(self, pos, state, num = 0):
        super().__init__()
        
        # if num == 1 or num == 0 or num ==2:
        if state == 'available':
            path = "./midia/number_" + str(num) + ".png"
        elif state == 'locked':
            path = "./midia/number_" + str(num) + "_unlocked" + ".png"
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        # else:
        #     self.image = pygame.Surface((64, 64))
        #     if state == 'available':
        #         self.image.fill('red')
        #     elif state == 'locked':
        #         self.image.fill('grey')
        self.rect = self.image.get_rect(center = pos)
        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('./midia/arrow.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)
        self.rect.y += 64
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, collected = False):
        super().__init__()
        if collected:
            self.image = pygame.image.load('./midia/coin/coin_01.png').convert_alpha()
        else:
            self.image = pygame.image.load('./midia/coin/unpicked_coin.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center = pos)