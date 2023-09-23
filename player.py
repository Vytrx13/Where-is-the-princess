import pygame
from sprite import *
from game_data import *
DASH_SPEED = 45
PLAYER_V0 = 6
GRAVITY = 10
class Player(pygame.sprite.Sprite):
    def __init__(self,pos, displaySurface):
        super().__init__()
        
        self.displaySurface = displaySurface

        self.particles = pygame.sprite.Group()
        
        # imports character sprites
        self.importCharacter()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations["idle"][self.frameIndex]
        
        self.rect = self.image.get_rect(topleft = pos)
        self.collideRect = pygame.Rect(self.rect.x+20,self.rect.y+14,24,48)
        
        
        
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.dashVerticalSentido = 0
        self.speed = PLAYER_V0
        self.gravity = 0.8
        self.jump_speed = -15
        self.dashFrame = 0
        
        self.canDash = True
        self.dashDelay = False
        self.jumpDelay = False
        
        self.upInput = False
        self.downInput = False
        self.rightInput = False
        self.leftInput = False
        
        
        #state
        self.state = "idle"
        self.facingRight = True
        self.onGround = True
        self.onRight = False
        self.onLeft = False
        self.isDashing = False
        
    def importCharacter(self):
        playerSheet = SpriteSheet("./midia/runner-sheet.png")
        playerSheetDash = SpriteSheet("./midia/runner-sheet_roxo2.png")
        self.animations = {"idle": [], "run": [], "jump": [], "jumpDash": []}
        
        for num in range(5):
            self.animations["idle"].append(playerSheet.get_image(num*SPRITE_SIDE, 0, SPRITE_SIDE, SPRITE_SIDE))
        for num in range(8):
            self.animations["run"].append(playerSheet.get_image(num*SPRITE_SIDE, SPRITE_SIDE, SPRITE_SIDE, SPRITE_SIDE))
        for num in range(4):
            self.animations["jump"].append(playerSheet.get_image(num*SPRITE_SIDE, SPRITE_SIDE*2, SPRITE_SIDE, SPRITE_SIDE))
        for num in range(4):
            self.animations["jumpDash"].append(playerSheetDash.get_image(num*SPRITE_SIDE, SPRITE_SIDE*2, SPRITE_SIDE, SPRITE_SIDE))
            
        self.dashSound = pygame.mixer.Sound("./midia/dash.wav")
        self.jumpSound = pygame.mixer.Sound("./midia/jump.wav")
            
    def animate(self):
        if self.state == "jump" and self.canDash:
            animation = self.animations["jumpDash"]
        else:
            animation = self.animations[self.state]
        
        #loop over index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        
        if self.facingRight:
            self.image = animation[int(self.frameIndex)]
        else:
            self.image = pygame.transform.flip(animation[int(self.frameIndex)], True, False).convert_alpha()
        
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        self.upInput = False
        self.downInput = False
        self.rightInput = False
        self.leftInput = False
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facingRight = True
            self.rightInput = True
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facingRight = False
            self.leftInput = True
        else:
            if not self.isDashing:
                self.direction.x = 0
            
        if (keys[pygame.K_z] or keys[pygame.K_y]) and self.onGround:
            if not self.jumpDelay:
                self.jump()
        
        if keys[pygame.K_DOWN]:
            self.dashVerticalSentido = 1
            self.downInput = True
        elif keys[pygame.K_UP]:
            self.dashVerticalSentido = -1
            self.upInput = True
        else:
            self.dashVerticalSentido = 0
            
            
        if keys[pygame.K_x]:
            self.toggleDash()
 
            
    def getState(self):
        # if self.direction.y < 0 or self.direction.y > 1:
        if not self.onGround:
            return "jump"
        elif self.direction.x != 0:
            return "run"
        else:
            return "idle"
        
        
        
    def jump(self):
        self.direction.y = self.jump_speed
        self.jumpSound.play()
        self.jumpDelay = True
        
                
    def turnOffGravity(self):
        self.gravity = 0
        self.gravityFrames = 0
            
    def turnOnGravity(self):  
        if self.gravity == 0:
            self.gravityFrames += 1
            if self.gravityFrames > 5:
                self.gravity = 0.8
    
            
    
    def update(self):
        if not self.isDashing:
            self.get_input()
        else:
            self.toggleDash()
        self.state = self.getState()
        self.animate()
        self.turnOnGravity()

        # self.apply_gravity()
        
    def toggleDash(self):
        if not self.isDashing and not self.onGround and not self.dashDelay:
            if self.canDash:
                self.isDashing = True
                self.dashDelay = True
                
                self.speed = DASH_SPEED * 0.75
                if not self.upInput and not self.downInput:
                    if self.facingRight:
                        self.direction.x = 1
                    else:
                        self.direction.x = -1
                
                self.direction.y = self.dashVerticalSentido * DASH_SPEED *0.3
                self.canDash = False
                particle = Particle(self.rect.center, "dash")
                self.particles.add(particle)
                self.dashSound.play()
        elif self.isDashing:
            
            if self.dashFrame > 5:
                self.isDashing = False
                
                self.turnOffGravity()
                self.direction.y /= 2
                
                self.speed = PLAYER_V0
                self.dashFrame = 0
            else:
                self.dashFrame += 1
    
    # def updateParticles(self, dx):
    #     self.particles.update(dx)
    #     self.particles.draw(self.displaySurface)


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos , type, size = 64):
        super().__init__()
        self.type = type
        self.frameIndex = 0
        self.animationSpeed = 0.5
        if self.type == "dash":
            self.particleSprite = pygame.image.load("./midia/dash_particles.png").convert_alpha()
            self.particleSprite = pygame.transform.scale(self.particleSprite, (size, size))
            
        elif self.type == "death":
            self.particleSprite = pygame.image.load("./midia/death_particles.png").convert_alpha()
            self.particleSprite = pygame.transform.scale(self.particleSprite, (size, size))
        
        self.image = self.particleSprite
        self.rect = self.image.get_rect(center = pos)
        
    def animate(self):
        self.frameIndex += self.animationSpeed
        if self.type == "dash":
            if self.frameIndex > 7:
                self.kill()
    
    def update(self, dx):
        self.animate()
        self.rect.x += dx
        
        

