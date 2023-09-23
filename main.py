import sys, pygame
from tile import Tile
from level import Level
from overworld import Overworld
from game_data import *
from player import *

class Game:
    def __init__(self):
        
        self.getSave()
        # self.maxLevel = 0
        # self.overworld = Overworld(1, self.maxLevel, screen)
        self.onLevel = False
        self.isPlayingMusic = False
        self.gameCompleted = False
        
        # self.playerDeathSound = pygame.mixer.Sound('./midia/death.wav')
        self.winSound = pygame.mixer.Sound('./midia/winsound.mp3')
        
        # self.deaths = 0
        
        # self.collectedCoins = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False}
        # self.coins = 0
        
    def getSave(self):
        # save = open("./config.txt", "r")
        # save = open("./config_inicial.txt", "r")
        save = open("./config.txt", "r")
        string = save.read()
        data = string.split("\n")
        self.maxLevel = int(data[0])
        self.deaths = int(data[1])
        self.dt = int(data[2])
        # print(self.dt)
        
        self.collectedCoins = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False}
        self.collectedCoins[0] = bool(int(data[3]))
        self.collectedCoins[1] = bool(int(data[4]))
        self.collectedCoins[2] = bool(int(data[5]))
        self.collectedCoins[3] = bool(int(data[6]))
        self.collectedCoins[4] = bool(int(data[7]))
        self.collectedCoins[5] = bool(int(data[8]))
        
        self.coins = 0
        for value in self.collectedCoins.values():
            if value:
                self.coins += 1
                
        save.close()
        
    def saveProgress(self):
        save = open("./config.txt", "w")
        save.write(str(self.maxLevel) + "\n")
        save.write(str(self.deaths) + "\n")
        save.write(str(self.dt) + "\n")
        save.write(str(int(self.collectedCoins[0])) + "\n")
        save.write(str(int(self.collectedCoins[1])) + "\n")
        save.write(str(int(self.collectedCoins[2])) + "\n")
        save.write(str(int(self.collectedCoins[3])) + "\n")
        save.write(str(int(self.collectedCoins[4])) + "\n")
        save.write(str(int(self.collectedCoins[5])) + "\n")
        save.close()
        
        
        
        
    def createLevel(self, levelData, currentLevel):
        # print("current level is " + str(currentLevel))
        self.level = Level(levelData, screen, currentLevel)
        self.onLevel = True
        self.level.levelCompleted = False
        self.level.levelFailed = False
        
    def createOverworld(self, currentLevel):
        self.overworld = Overworld(currentLevel, self.maxLevel, screen, self.collectedCoins)
        self.onLevel = False
        
    def endGame(self):
        if self.isPlayingMusic:
            pygame.mixer.music.stop()
        self.playMusic('./midia/overworld.mp3')
        
        
        
        
        if self.coins == 6:
            background = pygame.image.load('./midia/secret_ending.png').convert_alpha()
        else:
            background = pygame.image.load('./midia/ending.png').convert_alpha()
        
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0,0))
        
        
        
        # pygame.display.update()
        # pygame.time.wait(10000)
        # pygame.quit()
        
        self.gameCompleted = True
        
            
        
    def run(self):
        if self.onLevel:
            # passou de fase
            if self.level.levelCompleted:
                self.winSound.play()
                
                #coins
                if self.level.collectedCoin:
                    self.collectedCoins[self.overworld.currentLevel] = True
                    
                    #calculating coins
                    self.coins = 0
                    for value in self.collectedCoins.values():
                        if value:
                            self.coins += 1
                    # print(self.collectedCoins)
                
                if self.maxLevel < LEVELS_AMOUNT and self.overworld.currentLevel == self.maxLevel:
                    self.maxLevel += 1
                
                # beat game
                if self.maxLevel == LEVELS_AMOUNT and self.overworld.currentLevel == LEVELS_AMOUNT:
                    self.endGame()
                    
                self.onLevel = False
                self.createOverworld(self.maxLevel)
                self.playMusic('./midia/overworld.mp3')
                

                
            # falhou na fase
            elif self.level.levelFailed:
                # self.playerDeathSound.play()
                
                self.deaths += 1
                
                #restart level
                self.createLevel(levelsData[self.overworld.currentLevel], self.overworld.currentLevel)
                # self.level = Level(levelsData[self.overworld.currentLevel], screen)
                
            else:
                self.level.run()
        elif not self.onLevel:
            self.overworld.run()
    
    def playMusic(self, musicPath):
        if self.isPlayingMusic:
            pygame.mixer.music.stop()   
        pygame.mixer.music.load(musicPath)
        pygame.mixer.music.play(-1)
        self.isPlayingMusic = True

#setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Where is the Princess?')
game = Game()

# level = Level(level_map, screen)

#text
font = pygame.font.SysFont('calibri', 30)

#backgrounds
backgroundLevel = pygame.image.load('./midia/Background.png').convert_alpha()
backgroundLevel = pygame.transform.scale(backgroundLevel, (SCREEN_WIDTH, SCREEN_HEIGHT))

backgroundOverworld = pygame.image.load('./midia/logo.png').convert_alpha()
backgroundOverworld = pygame.transform.scale(backgroundOverworld, (SCREEN_WIDTH, SCREEN_HEIGHT))


currentLevel = 0
game.createOverworld(0)
game.playMusic('./midia/overworld.mp3')




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #salvando dados
            game.saveProgress()
            
            pygame.quit()
            sys.exit()
        if not game.onLevel:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    game.overworld.moveArrow("right")
                elif event.key == pygame.K_LEFT:
                    game.overworld.moveArrow("left")
                elif event.key == pygame.K_SPACE or event.key == pygame.K_z:
                    currentLevelData = levelsData[game.overworld.currentLevel]
                    game.createLevel(currentLevelData, game.overworld.currentLevel)
                    game.onLevel = True
                    game.playMusic('./midia/level'+ str(game.overworld.currentLevel) +  '.mp3')
                    
        else:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    game.createOverworld(game.level.currentLevel)
                    game.playMusic('./midia/overworld.mp3')
                
                if event.key == pygame.K_x:
                    for player in game.level.player:
                        player.dashDelay = False
                        
                if event.key == pygame.K_z or event.key == pygame.K_y:
                    for player in game.level.player:
                        player.jumpDelay = False
                        
                    
    
    if game.onLevel:
        screen.blit(backgroundLevel, (0,0))
    
    else:
        screen.blit(backgroundOverworld, (0,0)) 
    
    game.run()
    
    # level.run()
    
    # pygame.draw.rect(screen, 'red', level.player.sprite.collideRect, 1)
    if game.onLevel:
        pass
        # for enemy in game.level.enemies:
        #     pygame.draw.rect(screen, 'red', enemy.collideRect, 1)
        
        # pygame.draw.rect(screen, 'red', game.level.player.sprite.collideRect, 1)
    
    else:
        text = font.render("Unique coins: " + str(game.coins), True, "black")
        screen.blit(text, [SCREEN_WIDTH-200, 10])
    
    
    text = font.render("Deaths: " + str(game.deaths), True, "black")
    screen.blit(text, [185, 10])


    total_seconds = game.dt // FPS
            # Divide by 60 to get total minutes
    minutes = total_seconds // 60
    
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60
    
        # Use python string formatting to format in leading zeros
    output_string = "TIme: {0:02}:{1:02}".format(minutes, seconds)
    
        # Blit to the screen
    text = font.render(output_string, True, "black")
    screen.blit(text, [10, 10])
    
    game.dt += 1
    
    pygame.display.update()
    clock.tick(60)
    
    if game.gameCompleted:
        game.saveProgress()
        pygame.time.wait(15000)
        pygame.quit()
        sys.exit()
    
    