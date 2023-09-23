import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, type = "grass"):
        super().__init__()
        if type == "grass":
            self.image = pygame.image.load('./midia/grass_64x64.png').convert_alpha()
        elif type == "dirt":
            self.image = pygame.image.load('./midia/dirt_64x64.png').convert_alpha()
        elif type == "grass_dead":
            self.image = pygame.image.load('./midia/grass_dead_64x64.png').convert_alpha()
            
            
        self.image = pygame.transform.scale(self.image, (size, size))
        # self.image = pygame.Surface((size, size))
        # self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)
        
    # def update(self, dx):
    #     self.rect.x += dx
    
    def update(self, dx):
        self.rect.x += dx
        
        
        
class Text(pygame.sprite.Sprite):
    def __init__(self, message, pos, size, color = 'black'):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', size, bold=True)
        self.image = self.font.render(message, True, color)
        self.rect = self.image.get_rect(center = pos)
        
    def update(self, dx):
        self.rect.x += dx

    