# -*- coding: utf-8 -*-
"""
Dominick Smith

11-27-2023

Tanks!

A top down game where one player in a tank, fights off waves of enemy tanks for a high score
"""

import simpleGE, pygame, random

class Title (simpleGE.Scene):
    def __init__(self):
        super().__init__()
        
        self.background.fill((45, 61, 29))
        
        self.backgroundSound = simpleGE.Sound("TitleSong.wav")
        self.backgroundSound.play()
        
        self.addLabel()
        self.addButtons()
        self.addMultiLabel()
        
        self.sprites = [self.lblTitle, self.multiInstructions, self.btnStart, self.btnExit]
        
    def update(self):
        if self.btnStart.clicked:
            game = Game()
            game.start()
            self.stop()
            
        if self.btnExit.clicked:
            self.stop()
            
    def addLabel(self):
        self.lblTitle = simpleGE.Label()
        self.lblTitle.text = "Tanks: Pie Force"
        self.lblTitle.center = (300, 40)
        self.lblTitle.size = (450, 60)
        self.lblTitle.font = pygame.font.Font("Retro_Gaming.ttf", 40)
            
    def addMultiLabel (self):
        self.multiInstructions = simpleGE.MultiLabel()
        self.multiInstructions.textLines = [
            "Instructions:",
            "Use W A S D keys to move your Tank!",
            "Use Your MOUSE to aim and fire",
            "Eliminate the Enemy Tanks!",
            "Survive for as long as you can!",
            ]
        self.multiInstructions.size = (550,300)
        self.multiInstructions.center = (300, 225)
        self.multiInstructions.font = pygame.font.Font("Retro_Gaming.ttf", 15)
        
    def addButtons(self):
        self.btnStart = simpleGE.Button()
        self.btnStart.center = (150, 400)
        self.btnStart.text = "START"
        self.btnStart.font = pygame.font.Font("Retro_Gaming.ttf", 20)
        
        self.btnExit = simpleGE.Button()
        self.btnExit.center = (450,400)
        self.btnExit.text = "EXIT"
        self.btnExit.font = pygame.font.Font("Retro_Gaming.ttf", 20)
        
class Ending (simpleGE.Scene):
    def __init__(self):
        super().__init__()
        
        self.background.fill((45, 61, 29))
        
        self.backgroundSound = simpleGE.Sound("BattleTheme.wav")
        self.backgroundSound.play()
        
        self.addLabel()
        self.addButtons()
        
        
        self.sprites = [self.lblAgain, self.btnReset, self.btnExit, self.lblScore]
        
    def addLabel(self):
        self.lblAgain = simpleGE.Label()
        self.lblAgain.text = "Try again?"
        self.lblAgain.center = (320, 300)
        self.lblAgain.font = pygame.font.Font("Retro_Gaming.ttf", 15)
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"{Game().kills} tanks eliminated!"
        self.lblScore.center = (320,100)
        self.lblScore.font = pygame.font.Font("Retro_Gaming.ttf", 10)
        
    def addButtons(self):
        self.btnReset = simpleGE.Button()
        self.btnReset.center = (150, 400)
        self.btnReset.text = "RESET"
        self.btnReset.font = pygame.font.Font("Retro_Gaming.ttf", 20)
        
        self.btnExit = simpleGE.Button()
        self.btnExit.center = (450,400)
        self.btnExit.text = "EXIT"
        self.btnExit.font = pygame.font.Font("Retro_Gaming.ttf", 20)
        
    def update(self):
        if self.btnReset.clicked:
            game = Game()
            game.start()
            self.stop()
            
        if self.btnExit.clicked:
            self.stop()
        

class Game (simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.playerTank = PlayerTank(self)
        self.playerCannon = PlayerCannon(self)
        self.playerShell = PlayerShell(self)
        self.enemyShell = EnemyShell(self)
        self.keg = Keg(self)
        #self.enemyTank = EnemyTank(self)
        
        self.NUM_PlayerShells = 20
        self.currentPlayerShell = 0
        
        self.tmrDirChange = simpleGE.Timer()
        
        #self.backgroundSound = simpleGE.Sound("BattleTheme.wav")
        
        self.playerShells = []
        for i in range(self.NUM_PlayerShells):
            self.playerShells.append(self.playerShell)
        
        self.NUM_EnemyShells = 100
        self.CurrentEnemyShell = 0
        
        self.enemyShells = []
        for i in range(self.NUM_EnemyShells):
            self.enemyShells.append(self.enemyShell)
            
        self.lblHealth = simpleGE.Label()
        self.lblHealth.text = "0 %"
        self.lblHealth.center = (70,70)
        self.lblHealth.font = pygame.font.Font("Retro_Gaming.ttf", 15)
        
        self.lblShield = simpleGE.Label()
        self.lblShield.text = "0 % "
        self.lblShield.center = (70,40)
        self.lblShield.font = pygame.font.Font("Retro_Gaming.ttf", 15)
            
        self.currentRound = 0
        self.tanksRemaining = 0
        
        self.NUM_EnemyTanks = 100
        self.currentEnemyTank = 0
        
        self.enemyTank = []
        for i in range(self.NUM_EnemyTanks):
            self.enemyTank.append(EnemyTank(self))
        
        self.shield = 100
        self.health = 100
        
        self.kills = 0
        
        self.sprites = [self.playerTank, self.playerCannon, self.playerShell, self.enemyTank, self.enemyShell, self.lblHealth, self.lblShield, self.keg]
        
    def update(self):
        self.playerCannon.y = self.playerTank.y
        self.playerCannon.x = self.playerTank.x
            
        self.lblHealth.text = f"Health: {self.health} %"
        self.lblShield.text = f"Shield: {self.shield} %"
        
        if self.isKeyPressed(pygame.K_o):
           end = Ending()
           end.start()
           self.stop
        
        if self.health < 0 :
            self.health = 0
        
        if self.health == 0:
            end = Ending()
            end.start()
            self.stop()
        
        if self.tanksRemaining <= 0:
            self.currentRound += 1
            self.tanksRemaining = self.currentRound
            for i in range(self.tanksRemaining):
                self.currentEnemyTank += 1
                if self.currentEnemyTank >= self.NUM_EnemyTanks:
                    self.currentEnemyTank = 0
                self.enemyTank[self.currentEnemyTank].start()
                
        
    #def setY(self):
       
    
    #def setX(self):
        
        
class Keg (simpleGE.BasicSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        self.setImage("Keg.png")
        self.setSize(25,25)
        self.Respawn()
    
    def Respawn(self):
        newX = random.randint(0,640)
        newY = random.randint(0,480)
        self.x = newX
        self.y = newY
        
    def checkEvents(self):
        if self.collidesWith(self.scene.playerTank):
            if self.scene.shield < 100:
                self.scene.shield += 30
                if self.scene.shield > 100:
                    self.scene.shield = 100
                self.Respawn()       
        
        
class PlayerTank (simpleGE.SuperSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        scene.background = pygame.image.load("Tanks_Background.png") 
        scene.background = pygame.transform.scale (scene.background, (640,480))
        self.setImage("Tank-A-Base.png")
        self.boomSound = simpleGE.Sound("boom.wav")
        self.setSize(50,35)
        self.moveSpeed = 5
        self.y = 240
        self.x = 340
        self.setAngle(90)
        
    def checkEvents(self):
        if self.scene.isKeyPressed(pygame.K_a):
            self.turnBy(5)
        if self.scene.isKeyPressed(pygame.K_d):
            self.turnBy(-5)
        if self.scene.isKeyPressed(pygame.K_w):
            self.forward(5)
        if self.scene.isKeyPressed(pygame.K_s):
            self.forward(-3)
        
        if self.scene.shield < 0:
            self.scene.shield = 0
        
        if self.collidesWith(self.scene.enemyShell):
            if self.scene.shield >= 1:
                self.scene.shield -= 30
            else:
                self.scene.health -= 10
            self.boomSound.play()
        """if pygame.mouse .get_pressed() == (1, 0, 0):
            self.scene.currentPlayerShell += 1
            if self.scene.currentPlayerShell >= self.scene.NUM_PlayerShells:
                self.scene.currentPlayerShell = 0
            self.scene.playerShell[self.scene.currentPlayerShell].fire()"""
            
class PlayerCannon (simpleGE.SuperSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        self.setImage("TankTopRS.png")
        self.setSize(75,35)
        self.setAngle(90)
        
    def checkEvents(self):
        mousePos = pygame.mouse.get_pos()
        mouseDir = self.dirTo(mousePos)
        self.setAngle(mouseDir)
        
class PlayerShell (simpleGE.SuperSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        self.setImage("Shell.png")
        self.boomSound = simpleGE.Sound("boom.wav")
        self.setSize(20,9)
        self.setAngle(90)
        self.hide()
        self.setBoundAction(self.HIDE)
        
    def checkEvents(self):
        if self.visible == False:
            if pygame.mouse .get_pressed() == (1, 0, 0):
                self.fire()
                
        if self.collidesWith(EnemyTank(self.scene)):
           self.hide()  
            
    def fire(self):
        self.show()
        self.setPosition(self.scene.playerCannon.rect.center)
        mousePos = pygame.mouse.get_pos()
        mouseDir = self.dirTo(mousePos)
        self.setAngle(mouseDir)
        self.setSpeed(10)
        self.boomSound.play()
        
            
        """if self.x >= 640:
            self.reset()
        if self.x <= 0:
            self.reset()
        if self.y >= 480:
            self.reset()
        if self.y <= 0:
            self.reset()"""
                       
    def reset(self):
        self.hide()
        
class EnemyTank (simpleGE.SuperSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        self.setImage("EnemyTank.png")
        self.setSize(35,35)
        self.moveSpeed = 5
        
        self.boomSound = simpleGE.Sound("boom.wav")
        
        self.hide()
        """positivePossibility = random.randint(0,100)
        negativePossibility = random.randint(380,480)
        choice = random.randint(0,1)
        if choice == 0:
            goodY = positivePossibility
        if choice == 1:
            goodY = negativePossibility
    
        positivePossibility = random.randint(0,150)
        negativePossibility = random.randint(490,640)
        choice = random.randint(0,1)
        if choice == 0:
            goodX = positivePossibility
        if choice == 1:
            goodX = negativePossibility
        
        self.y = goodY
        self.x = goodX
        self.setAngle(90)
        self.setSpeed(.5)
        
        self.HP = 100"""
        """self.scene.currentEnemyTank += 1
        for i in range(self.scene.tanksRemaining):
            if self.scene.currentEnemyTank >= self.scene.NUM_EnemyTanks:
                self.scene.currentEnemyTank = 0
            self.scene.enemyTank[self.scene.currentEnemyTank].start()"""
        
    def checkEvents(self):
        zeroPos = self.dirTo((self.scene.playerTank.x, self.scene.playerTank.y))
        self.setAngle(zeroPos)
        if self.collidesWith(self.scene.playerShell):
            self.HP -= random.randint(20,25)
            if self.HP <= 0:
                self.hide()
                self.scene.tanksRemaining -=1
                self.scene.kills += 1
            self.boomSound.play()

    
    def start(self):
        self.HP = 100
        self.show()
        
        positivePossibility = random.randint(0,100)
        negativePossibility = random.randint(380,480)
        choice = random.randint(0,1)
        if choice == 0:
            goodY = positivePossibility
        if choice == 1:
            goodY = negativePossibility
        
        positivePossibility = random.randint(0,150)
        negativePossibility = random.randint(490,640)
        choice = random.randint(0,1)
        if choice == 0:
            goodX = positivePossibility
        if choice == 1:
            goodX = negativePossibility
        
        self.y = goodY
        self.x = goodX
        zeroPos = self.dirTo((320,240))
        self.setAngle(zeroPos)
        self.setSpeed(.5)

        
        
class EnemyShell (simpleGE.SuperSprite):
    def __init__ (self, scene):
        super().__init__(scene)
        self.setImage("Shell.png")
        self.setSize(20,9)
        self.setAngle(90)
        self.boomSound = simpleGE.Sound("boom.wav")
        self.hide()
        self.setBoundAction(self.CONTINUE)
        
    def checkEvents(self):
        fireChance = random.randint(1,100)
        if fireChance == 1:
            self.EnemyFire()
        if self.collidesWith(self.scene.playerTank):
            self.hide()
            
    def EnemyFire(self):
        self.show()
        self.setPosition(self.scene.enemyTank[self.scene.currentEnemyTank].rect.center)
        selfDir = self.dirTo((self.scene.playerTank.x, self.scene.playerTank.y))
        self.setAngle(selfDir)
        self.setSpeed(10)
        self.boomSound.play()
        
def main():
    title = Title()
    title.start()
    
if __name__ == "__main__":
    main()