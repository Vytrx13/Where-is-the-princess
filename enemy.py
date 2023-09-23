import pygame
from game_data import *
from sprite import SpriteSheet
from game_data import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size = tile_size, type = "ball", change_x = 0, change_y = 0, period = 1):
        super().__init__()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.type = type
        self.pos = pos
        self.size = size
        self.animations = []
        
        self.period = period
        self.change_x = change_x
        self.change_y = change_y
        self.frames = 0
        
        self.setupEnemy()


        
    def setupEnemy(self):
        if self.type == "ball":
            self.image = pygame.image.load('./midia/ball.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        
            self.rect = self.image.get_rect(topleft = self.pos)
            self.collideRect = pygame.Rect(self.rect.x + 13, self.rect.y + 17, self.rect.width - 22, self.rect.height - 30)
        
        
        if self.type == "saw":
            enemySheet = SpriteSheet("./midia/saw38x38.png") 
            
            for num in range(8):
                self.animations.append(enemySheet.get_image(num* 38, 0, 38, 38))
                
            self.image = self.animations[0]
            self.rect = self.image.get_rect(topleft = self.pos)
            self.collideRect = pygame.Rect(self.rect.x + 12, self.rect.y + 11, self.rect.width - 22, self.rect.height - 22)
    
    def animate(self):
        if len(self.animations) > 0:
            #loop over index
            self.frameIndex += self.animationSpeed
            
            if self.frameIndex >= len(self.animations):
                self.frameIndex = 0
                
            self.image = self.animations[int(self.frameIndex)]
            self.image = pygame.transform.scale(self.image, (self.size, self.size)).convert_alpha()
            
    def move(self):
        self.frames += 1
        if self.frames % int(self.period*FPS) == 0:
            if self.type == "saw":
                self.change_x *= -1
                self.change_y *= -1
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.collideRect.x += self.change_x
        self.collideRect.y += self.change_y
    
    def update(self, dx):
        self.animate()
        self.move()
        self.rect.x += dx
        self.collideRect.x += dx
