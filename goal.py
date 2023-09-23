import pygame
from game_data import *
from sprite import SpriteSheet

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, size = tile_size):
        super().__init__()
        
        self.importGoal()
        
        self.animationSpeed = 0.15
        self.frameIndex = 0
        
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft = pos)
        
    def importGoal(self):
        goalSheet = SpriteSheet("./midia/goal.png")
        self.animations = []
        
        for num in range(4):
            self.animations.append(goalSheet.get_image(num* SPRITE_SIDE, 0, SPRITE_SIDE, SPRITE_SIDE))
            
    
    def animate(self):
        
        
        #loop over index
        self.frameIndex += self.animationSpeed
        
        if self.frameIndex >= len(self.animations):
            self.frameIndex = 0
            
        self.image = self.animations[int(self.frameIndex)].convert_alpha()
        
       

        
    def update(self, dx):
        self.rect.x += dx
        
        
class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, size = tile_size/2):
        super().__init__()
        
        self.importCoin()
        
        
        self.animationSpeed = 0.15
        self.frameIndex = 0
        
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft = pos)
        
        
    def importCoin(self):
        
        
        for num in range(4):
            self.animations = []
            coinsprite = SpriteSheet("./midia/coins_animation.png")
            
            for num in range(8):
                self.animations.append(coinsprite.get_image(num* 16, 0, 16, 16))
            # for num in range(1,9):
            #     self.animations.append(pygame.image.load("./midia/coin/coin_0" + str(num) + ".png").convert_alpha())
            
                
    
    def animate(self):
        
        
        #loop over index
        self.frameIndex += self.animationSpeed
        
        if self.frameIndex >= len(self.animations):
            self.frameIndex = 0
            
        self.image = self.animations[int(self.frameIndex)].convert_alpha()
        
        
    def update(self, dx):
        self.rect.x += dx
        
class Orb(pygame.sprite.Sprite):
    def __init__(self, pos, size = tile_size/2):
        super().__init__()
        
        self.image = pygame.image.load("./midia/orb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(size), int(size)))
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self, dx):
        self.rect.x += dx
                
    
            
        