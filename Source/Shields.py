# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import random
import os
from pygame.color import THECOLORS
import sys    # for testing
from pygame.locals import *

import enviro # my global game environment
import Noise
from FloatingSprite import FloatingSprite
from AttackerStuff import *
from YourStuff import FuelStuff # for testing


class Shields(pygame.sprite.Sprite):
    def __init__(self, image_file, increasing_file, initFuelBays):
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = 10
        
        self.increasingImage = pygame.image.load(os.path.join(enviro.artPathHack,increasing_file)).convert_alpha()
        
##        self.shieldBlue = []
##        self.shieldRed = []
##        self.shieldMaxRed = []
##
##        for i in range(0, 10):
##            self.shieldBlue.append(0)
##            self.shieldRed.append(0)
##            self.shieldMaxRed.append(i*(150/15))
            
        #self.fuelBaysAvailable = 1  # great idea for upgrade potential!
        self.fuelBay = initFuelBays
        self.fuelPerPellet = enviro.FUEL_PER_PELLET

        self.promises = 0
        
        #self.consuming = self.fuelPerPellet
        self.consuming = 0
        self.consumingBay = 0
        
        self.upgrades = enviro.shieldUpgrades
                
        self.initUpgrades()
        self.cooldown = self.cooldown_period
        self.poweringUp = 0
        self.needHum = True
        
    def initUpgrades(self):
        self.shieldBlue = []
        self.shieldRed = []
        self.shieldMaxRed = []

        for i in range(0, 10):
            self.shieldBlue.append(0)
            self.shieldRed.append(0)
            self.shieldMaxRed.append(i*(150/15))        
        
        self.cooldown_period = enviro.SHIELD_COOLDOWN
        for i in range (0,self.upgrades):
            self.applyUpgrade() 
        
        
    def paintPad(self):
        pass        

    def upgrade(self):
        if self.upgrades < 11:
            self.upgrades = self.upgrades + 1
            enviro.shieldUpgrades = self.upgrades
            self.repaint()
            self.applyUpgrade()
            return True
        return False
    
    def applyUpgrade(self):
        self.cooldown_period = self.cooldown_period - 10
        if self.cooldown_period < 0:
            self.cooldown_period == 0
        enviro.BOMB_POWER = enviro.BOMB_POWER - 40
        if enviro.BOMB_POWER < 100:
            enviro.BOMB_POWER = 100 
        #print "cooldown period=", self.cooldown_period
        #print "bomb power", enviro.BOMB_POWER
        
    def paint(self, location, fuelPile):
        self.fuelPile = fuelPile
        self.rect.left = location[0]
        self.rect.top = location[1]
        
        enviro.screen.blit(self.image, self.rect)
        
        self.fuelPile[self.fuelBay[1]].paint([525,494])
        self.fuelPile[self.fuelBay[0]].paint([552,494])
        self.fuelPile[self.fuelBay[2]].paint([579,494])
        
        left = self.rect.left
        top = self.rect.top        
        
        pygame.draw.rect(enviro.screen, THECOLORS["blue"], [left+4,top+71,80,9], 0)
        for i in range(0, self.upgrades):
            pygame.draw.rect(enviro.screen, [130,202,253], [left+6+i*7,top+73,5,5], 0)        
        
        
    def repaint(self):
        enviro.screen.blit(self.image, self.rect)
        
        self.fuelPile[self.fuelBay[1]].paint([525,494])
        self.fuelPile[self.fuelBay[0]].paint([552,494])
        self.fuelPile[self.fuelBay[2]].paint([579,494])
        
        left = self.rect.left
        top = self.rect.top        
        
        pygame.draw.rect(enviro.screen, THECOLORS["blue"], [left+4,top+71,80,9], 0)
        for i in range(0, self.upgrades):
            pygame.draw.rect(enviro.screen, [130,202,253], [left+6+i*7,top+73,5,5], 0)        
        

    def hitShield(self, power):
        for i in range(0,10):
            self.shieldRed[i] = 0
            self.shieldBlue[i] = 0        
        color = power
        shieldBar = 9
        while color > 215:
            self.shieldBlue[shieldBar] = 215
            color = color - 215
            shieldBar = shieldBar - 1
        if shieldBar > -1:
            self.shieldBlue[shieldBar] = color
            

    # Paint the shield on the screen, and produce a sprite as big as it is
    def paintShield(self, power):
        color=power
        shieldBar = 9
        for i in range(0,10):
            self.shieldRed[i] = 0
        #print "painting shields with power=",power
        while color > 215:
            self.shieldBlue[shieldBar] = 215
            shieldBar = shieldBar - 1
            for j in range (shieldBar+1,10):
                self.shieldRed[j] = self.shieldRed[j] + 15
                if self.shieldRed[j] > self.shieldMaxRed[j]:
                   self.shieldRed[j] = self.shieldMaxRed[j]
            if shieldBar == -1:
                color = 215
                #print "Max shields =",power
                break
            color = color - 215
        if shieldBar > -1:
            self.shieldBlue[shieldBar] = color
    
        shim = 0
        shieldHeight = 0
        shieldTop = 999
        for i in range(9,-1,-1):
            shim = 9-i+shim+4
            if self.shieldBlue[i]>0:
                shieldHeight = shieldHeight + (i+3)
                if shieldTop > (275+i*15)+shim:
                    shieldTop = (275+i*15)+shim
            if self.shieldBlue[i] > 0:
                pygame.draw.rect(enviro.screen, [self.shieldRed[i],0,self.shieldBlue[i]+40], 
                   [400,(275+i*15)+shim,330,i+3],0)
        #print "Power:", power, "Shield top:",shieldTop,"height:", shieldHeight
        if power == 2050:
            pygame.draw.lines(enviro.screen, [200,200,200], False, [ [400,359], [729,359] ], 1)
            
        shieldSprite = ShieldSprite(self.theImage, 400,shieldTop, 330, shieldHeight)
        #shieldSprite.paint()
        return shieldSprite
        
    def powerUp(self, power, fuelPile):
        pygame.draw.rect(enviro.screen, [0,0,0], [520,427,90,24], 0) # clear the powerup indicator
        if self.consuming > 0:
            if power < enviro.SHIELD_MAX:
                enviro.screen.blit(self.increasingImage, [520,426])
                
                if self.needHum:
                    #self.powerUpAnimationLine = 420
                    self.powerUpAnimationLine = 9
                    self.needHum = False
                    #print "Play the hum"
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.SHIELD_HUM])
                    else:
                        print "no channel for shield hum sound, will try to use main"
                        enviro.soundEffect[Noise.SHIELD_HUM].play()
                # Dr. Bart had me add this cool animation... not bad!
                self.powerUpAnimationLine -= 1
                if self.powerUpAnimationLine < 0:
                    self.powerUpAnimationLine = 9
                
                for i in range(self.powerUpAnimationLine, 27,10):
                     pygame.draw.lines(enviro.screen, [0,0,0], False, [[520,self.powerUpAnimationLine+i+416],[610,self.powerUpAnimationLine+i+416]], 3)
                
                power = power + enviro.SHIELD_POWER_PER_CYCLE
                if power > enviro.SHIELD_MAX:
                    power = enviro.SHIELD_MAX
                self.consuming = self.consuming - 1
            
        if self.consuming == 0 and power < enviro.SHIELD_MAX + 1:
            if self.cooldown > 0:
                self.cooldown = self.cooldown - 1
            else:
                
#                self.poweringUp = self.poweringUp + 1
#                if self.poweringUp > enviro.SHIELD_INCREASE_PER_CYCLE:
                self.cooldown = self.cooldown_period
                self.needHum = True
#                   self.poweringUp = 0
            
            
                if self.fuelBay[self.consumingBay] > 0:
                   self.consuming = self.fuelPerPellet
                   self.fuelBay[self.consumingBay] = self.fuelBay[self.consumingBay] - 1
                   self.repaint()
                else:
                    for i in range(0,3):
                        if self.fuelBay[i] > 0:
                            self.consumingBay = i

        return power
    
    def loadFuel(self):
        loadBay = -1
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                loadBay = i
        if loadBay > -1:
            self.fuelBay[loadBay] = 10
            self.promises = self.promises - 1
            self.repaint()
            return True
        return False

    def unloadStuff(self):

        for i in range(0,3):
            if self.fuelBay[i] == 10:
                self.fuelBay[i] = 0
                self.repaint()
                return True
        return False    
    
    
    def promiseRefuel(self):
        self.promises = self.promises + 1

    # See if we need more fuel for shields
    def needFuel(self):
        emptyBays = 0
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                emptyBays += 1
        if emptyBays > self.promises:
            return True
        return False
    
    def nearlyEmpty(self):
        if enviro.laserRefuelDisabled:
            return False
        
        emptyBays = 0
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                emptyBays += 1
        if emptyBays < 2:
            return False
        if emptyBays > self.promises:
            return True
        return False      
    
if __name__ == '__main__':
    
    print "TEST: shields"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
# stuff needed for init:
    fuelPile = []

    for i in range(0,11):
        fuelFile = "fuelStore" + str(i) + ".png"
        fuelState = FuelStuff(fuelFile)
        fuelPile.append(fuelState)
        
    dramaBackground = \
        pygame.image.load(os.path.join(enviro.artPathHack,'dramaBackground.png'))    
 
    shieldsFile = "shields.png"
    shieldsIncreasingFile = "shieldsUp.png"
    
##    soundEffect = []
##    soundEffect.append(Noise.load_sound('25322_Therac_25_starshiphum.wav'))
##    Noise.SHIELD_HUM = len(soundEffect) - 1  

    enviro.init()
    enviro.start("Easy")
    
    s = Shields(shieldsFile, shieldsIncreasingFile, [10,10,10])
    s.paint([520,450], fuelPile)
    shieldPower = 2050

    while True:
        hit = False
        enviro.screen.blit(dramaBackground, [400,0,330,449])          
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                    
            if event.type == pygame.KEYDOWN: 
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()                
                if event.key == pygame.K_h:
                    print "hit"
                    hit = True
                  
                    
                if event.key == pygame.K_f:
                    print "load fuel"
                    s.loadFuel()
                if event.key == pygame.K_u:
                    print "upgrade"
                    s.upgrade()                    
##            if event.key == pygame.K_h:
##                print "hit"
##                s.hitShield(power)
##                power = power - 10
                   
                    
                  
        
        shieldPower= s.powerUp(shieldPower, enviro.fuelPile)            
        shieldSprite = s.paintShield(shieldPower) 
        
        if hit:
            shieldPower = shieldPower - enviro.BOMB_POWER
            if shieldPower < 0:
                shieldPower = 0
            s.hitShield(shieldPower)
            s.paintShield(shieldPower)            
             
        
        myClock.tick(30)
        pygame.display.flip()         
     
    