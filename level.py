import pygame
from tile import *
from player import *
from goal import *
from game_data import *
from enemy import Enemy

PLAYER_LIMIT_X = SCREEN_WIDTH / 2
# PLAYER_LIMIT_Y = SCREEN_HEIGHT / 3

class Level:
    
    def __init__(self, currentLevelData, surface, currentLevel):
        self.currentLevel = currentLevel
        # print(self.currentLevel)
        self.display_surface = surface
        self.setup_level(currentLevelData)
        
        self.coinPickupSound = pygame.mixer.Sound('./midia/coin_pickup.wav')
        self.orbPickupSound = pygame.mixer.Sound('./midia/orb_pickup.wav')
        
        
        self.world_shift = 0
        
        self.colision_x = 0
        
        self.dx = 0
        
        self.collectedCoin = False
        
        self.dead = False
        self.deadFrame = 0
        
        
    #setup  
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.coin = pygame.sprite.GroupSingle()
        self.orbs = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        
        #gerando os tiles com base no layout
        
        for row_i, row in enumerate(layout):
            # print(row_i, row)
            
            for col_i, cell in enumerate(row):
                
                # print(row_i, row, col_i, cell)
                x = col_i * tile_size
                y = row_i * tile_size
                
                #criando os tiles
                if cell == 'G':
                    tile = Tile((x,y),tile_size, "grass")
                    self.tiles.add(tile)
                    
                if cell == 'D':
                    tile = Tile((x,y),tile_size, "dirt")
                    self.tiles.add(tile)
                
                if cell == 'g':
                    tile = Tile((x,y),tile_size, "grass_dead")
                    self.tiles.add(tile)
                if cell == "W":
                    goal = Goal((x,y), tile_size)
                    self.goal.add(goal)
                
                if cell == "C":
                   
                    coin = Coin((x,y), tile_size)
                    self.coin.add(coin)
                
                # enemies
                if cell == "B":
                    enemy = Enemy((x,y), tile_size, "ball")
                    self.enemies.add(enemy)
                if cell == "S":
                    enemy = Enemy((x,y), tile_size, "saw", 5, 0, 1.5)
                    self.enemies.add(enemy)
                    
                #orb
                if cell == "R":
                    orb = Orb((x,y))
                    self.orbs.add(orb)
                    
                #localizer
                if cell == 'L':
                    print("localizer: ", x /tile_size, y/tile_size)
                    
                
                    
                #criando o player
                if cell == 'P':
                    player_sprite = Player((x,y), self.display_surface)
                    self.player.add(player_sprite)
        
        #specific setup for each level
        
        # LEVEL 0
        if self.currentLevel == 0:
            
            # text = Text("batata", (16*tile_size, 7*tile_size), 30, 'orange')
            # self.texts.add(text)
            
            text = Text("TUTORIAL", (4*tile_size, 4*tile_size), 60, 'red')
            self.texts.add(text)
            
            text = Text("Use the left and right arrow keys to move", (4*tile_size, 7*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("Press z to jump", (14*tile_size, 7*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("When you're not on the ground, press x to dash", (30*tile_size, 1*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("The dash direction is controlled by the arrow keys", (30*tile_size, 3*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("You can dash vertically, horizontally or diagonally", (30*tile_size, 4*tile_size), 20, 'white')
            self.texts.add(text)
            
            text = Text("You can only dash once until you get to the ground again", (30*tile_size, 5*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("You'll know that you can dash if the character is pinkish", (30*tile_size, 7*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("The coins are optional, but you should try collecting them", (48*tile_size, 5*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("You can always leave the level and return to overworld by pressing esc", (65*tile_size, 3*tile_size), 30, 'white')
            self.texts.add(text)
            
            text = Text("Now then, good luck on saving the princess or whatever :)", (65*tile_size, 5*tile_size), 40, 'white')
            self.texts.add(text)
        # LEVEL 1
        if self.currentLevel == 1:
            text = Text("LEVEL 1", (4*tile_size, 4*tile_size), 60, 'blue')
            self.texts.add(text)
            
            text = Text("Let's get started with an easy one", (4*tile_size, 6*tile_size), 30, 'blue')
            self.texts.add(text)
            
            
            
        # LEVEL 2
        if self.currentLevel == 2:
            text = Text("LEVEL 2", (4*tile_size, 4*tile_size), 60, 'red')
            self.texts.add(text)
            
            text = Text("This one is kinda hard", (4*tile_size, 1*tile_size), 30, 'red')
            self.texts.add(text)
            
            
            enemy = Enemy((12*tile_size, 5.5*tile_size), tile_size, "saw", -5, 0, 1.5)
            self.enemies.add(enemy)
            
            enemy = Enemy((20*tile_size, 6*tile_size), tile_size, "saw", 0, 4, 1)
            self.enemies.add(enemy)
            
            enemy = Enemy((24*tile_size, 10*tile_size), tile_size, "saw", 0, -4, 1)
            self.enemies.add(enemy)
            
            enemy = Enemy((29*tile_size, 9*tile_size), tile_size, "saw", 0, -3, 2)
            self.enemies.add(enemy)
          
        # LEVEL 3  
        if self.currentLevel == 3:
            orb = Orb((16.8*tile_size, 5*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((46.2*tile_size, 4.5*tile_size), tile_size*0.7)
            self.orbs.add(orb)
                
            orb = Orb((48.4*tile_size, 3.4*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((52.4*tile_size, 4.4*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((76*tile_size, 5*tile_size), tile_size*0.7)
            self.orbs.add(orb)
            
            orb = Orb((71*tile_size, 7*tile_size), tile_size*0.7)
            self.orbs.add(orb)
            
            
            text = Text("New mechanic! Orbs reset your dash", (6*tile_size, 6*tile_size), 30, 'purple')
            self.texts.add(text)
            
            text = Text("LEVEL 3", (4*tile_size, 10*tile_size), 60, 'purple')
            self.texts.add(text)
        
        # LEVEL 4
        if self.currentLevel == 4:
            orb = Orb((52.5*tile_size, 4.5*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((56.3*tile_size, 2.5*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((56.3*tile_size, 4.5*tile_size))
            self.orbs.add(orb)
            
            enemy = Enemy((31*tile_size, 1*tile_size), tile_size, "saw", 0, 4, 1.875)
            self.enemies.add(enemy)
            
            enemy = Enemy((33*tile_size, 2*tile_size), tile_size, "saw", 0, 6, 1.25)
            self.enemies.add(enemy)
            
            enemy = Enemy((35*tile_size, 1*tile_size), tile_size, "saw", 0, 3, 2.5)
            self.enemies.add(enemy) 
            
            enemy = Enemy((37*tile_size, 2*tile_size), tile_size, "saw", 0, 2, 3.75)
            self.enemies.add(enemy)
            
            enemy = Enemy((39*tile_size, 1*tile_size), tile_size, "saw", 0, 5, 1.5)
            self.enemies.add(enemy)
            
            text = Text("LEVEL 4", (59*tile_size, 8*tile_size), 60, 'green')
            self.texts.add(text)
            
        # LEVEL 5
        if self.currentLevel == 5:
            enemy = Enemy((33*tile_size, 4*tile_size), tile_size, "saw", 2, 0, 1)
            self.enemies.add(enemy)
            
            orb = Orb((24.3*tile_size, 8.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((31.3*tile_size, 6.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((49.3*tile_size, 1.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((53.3*tile_size, 1.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((49.3*tile_size, 3.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((45.3*tile_size, 5.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((49.3*tile_size, 5.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((41*tile_size, 9.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((45.3*tile_size, 9.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((45.3*tile_size, 7.3*tile_size))
            self.orbs.add(orb)
            
            orb = Orb((51.3*tile_size, 6.3*tile_size))
            self.orbs.add(orb)
            
            text = Text("LEVEL 5", (3*tile_size, 10*tile_size), 60, 'blue')
            self.texts.add(text)
            
            text = Text("Precision shall be necessary for this one", (1*tile_size, 4*tile_size), 30, 'blue')
            self.texts.add(text)
            
            text = Text("The princess is close!", (1*tile_size, 2*tile_size), 30, 'blue')
            self.texts.add(text)
            
            
            
                
    
    def scroll_x(self):
        player = self.player.sprite
        # player_x = player.collideRect.centerx
        # direction_x = player.direction.x
        
        
        if player.collideRect.centerx < PLAYER_LIMIT_X :
            self.dx = PLAYER_LIMIT_X - player.collideRect.centerx
            player.collideRect.centerx = PLAYER_LIMIT_X
            player.rect.x = player.collideRect.x - 20
            self.tiles.update(self.dx)
            self.goal.update(self.dx)
            # self.enemies.update(self.dx)
            self.coin.update(self.dx)
            self.orbs.update(self.dx)
            self.texts.update(self.dx)
            
            
        elif player.collideRect.centerx > SCREEN_WIDTH - PLAYER_LIMIT_X :
            self.dx = SCREEN_WIDTH - PLAYER_LIMIT_X - player.collideRect.centerx
            player.collideRect.centerx = SCREEN_WIDTH - PLAYER_LIMIT_X
            player.rect.x = player.collideRect.x - 20
            self.tiles.update(self.dx)
            self.goal.update(self.dx)
            # self.enemies.update(self.dx)
            self.coin.update(self.dx)
            self.orbs.update(self.dx)
            self.texts.update(self.dx)
            
            
    def horizontalMovement(self):
        player = self.player.sprite
        
        # if not player.collideRect.centerx < SCREEN_WIDTH / 4 or player.collideRect.centerx > SCREEN_WIDTH - (SCREEN_WIDTH / 4):
        player.rect.x += player.direction.x * player.speed
        player.collideRect.x += player.direction.x * player.speed
        
        self.scroll_x()
        # if player.collideRect.centerx < PLAYER_LIMIT_X:
        #     player.collideRect.centerx = PLAYER_LIMIT_X
        #     player.rect.x = player.collideRect.x - 20
            
        # elif player.collideRect.centerx > SCREEN_WIDTH - PLAYER_LIMIT_X:
        #     player.collideRect.centerx = SCREEN_WIDTH - PLAYER_LIMIT_X
        #     player.rect.x = player.collideRect.x - 20
        
        
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collideRect):
                
                #colisao na esquerda
                if player.direction.x < 0:
                    player.collideRect.left = sprite.rect.right 
                    player.rect.left = player.collideRect.left - 20
                    player.onLeft = True
                    self.colision_x = player.collideRect.left 
                    # print("colisao na esquerda\n")
                    
                #colisão na direita
                elif player.direction.x > 0:
                    # self.levelCompleted = True
                    player.collideRect.right = sprite.rect.left 
                    player.rect.left = player.collideRect.left - 20
                    player.onRight = True
                    self.colision_x = player.collideRect.right
                    # print("colisao na direita\n")
        
        
        

        #passou de nivel
        for goal in self.goal:
            if goal.rect.colliderect(player.collideRect):
                self.levelCompleted = True
                
        #morreu
        for enemy in self.enemies:
            if enemy.collideRect.colliderect(player.collideRect):
                self.playerDied()
                
                
                
        #pegou moeda    
        for coin in self.coin:
            if coin.rect.colliderect(player.collideRect):
                self.collectedCoin = True
                coin.kill()
                self.coinPickupSound.play()
                
        #pegou orb
        for orb in self.orbs:
            if orb.rect.colliderect(player.collideRect):
                self.orbPickupSound.play()
                player.canDash = True
                orb.kill()
                     
                    
    def verticalMovement(self):
        player = self.player.sprite
        
        if not player.isDashing:
            player.direction.y += player.gravity
        player.rect.y += player.direction.y
        player.collideRect.y += player.direction.y
        # player.apply_gravity()
        
        

        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collideRect) : 
                if player.direction.y < 0 and -50 <= sprite.rect.bottom - player.collideRect.top <= 50:
                    player.collideRect.top = sprite.rect.bottom
                    player.rect.top = player.collideRect.top - 14
                    
                elif player.direction.y > 0 and -50 <= sprite.rect.top - player.collideRect.bottom <= 50:
                    player.collideRect.bottom = sprite.rect.top
                    player.rect.top = player.collideRect.top - 14
                    player.onGround = True
                    player.canDash = True
                player.direction.y = 0
        
        
                
                
                
        if player.onGround and (player.direction.y < 0 or player.direction.y > 1):
            player.onGround = False
            
        for goal in self.goal:
            if goal.rect.colliderect(player.collideRect):
                self.levelCompleted = True
                # print("level completed\n")
                
        for enemy in self.enemies:
            if enemy.collideRect.colliderect(player.collideRect):
                self.playerDied()
                
                # print("level failed\n")
                
        if player.collideRect.top > SCREEN_HEIGHT:
            self.playerDied()
            
                    
    def playerDied(self):
        if not self.dead:
            self.dead = True
            pygame.mixer.Sound('./midia/death.wav').play()
            
            particle = Particle((self.player.sprite.rect.x, SCREEN_HEIGHT/2), "death", 320)
            self.particles.add(particle)
        
        
    
    def run(self):
        self.dx = 0
        
        
        
        #atualizando os tiles e goal e coin
        self.tiles.draw(self.display_surface)
        
        for goal in self.goal:
            goal.animate()
        self.goal.draw(self.display_surface)
        
        for coin in self.coin:
            coin.animate()
        self.coin.draw(self.display_surface)
        
        #orb
        self.orbs.draw(self.display_surface)
        
        #text
        self.texts.draw(self.display_surface)

        #atualizando o player
        
        if not self.dead:
            
            self.player.update()   
            self.horizontalMovement()
            self.verticalMovement()
            self.player.sprite.particles.update(self.dx)
            self.player.sprite.particles.draw(self.display_surface)
            self.player.draw(self.display_surface)
            
        else:
            if self.deadFrame >= 20:
                self.levelFailed = True
            else:
                self.deadFrame += 1

        
        # atualizando enemies
        self.enemies.update(self.dx)
        self.enemies.draw(self.display_surface)
        
        #level particles
        
        self.particles.draw(self.display_surface)
        

        
               
        

        
        
    
    
    