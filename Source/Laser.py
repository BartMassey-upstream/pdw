# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
#not sure all of these are needed...
import sys
import os
import pygame
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise
    
from AttackerStuff import ShieldSprite
from YourStuff import TargetSprite
from YourStuff import FuelStuff # for testing


class Laser(pygame.sprite.Sprite):
    def __init__(self, image_file):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = 11
        
        self.state = "Armed"
        self.aimCount = 0
        
        self.fuelBay = [10,10,10]
        self.promises = 0
        
        self.consuming = enviro.LASER_PER_PELLET
        self.consumingBay = 0
##        self.upgrades = init_Upgrades
##        for i in range(0,self.upgrades):
##            self.applyUpgrade()
        self.upgrades = enviro.laserUpgrades
        self.initUpgrades() # I added continue/restart too late, killing me now
            
    def initUpgrades(self):
        self.laserPower = enviro.LASER_UPGRADE_POWER
        self.aimTime = enviro.LASER_AIM_TIME
        for i in range(0,self.upgrades):
            self.applyUpgrade()        
            
    def paintPad(self):
        pass
        
    def paint(self, location, fuelPile):
        self.myFuelPile = fuelPile
        
        self.rect.left = location[0]
        self.rect.top = location[1]
        
        enviro.screen.blit(self.image, self.rect)
        
        left = self.rect.left
        top = self.rect.top
        self.myFuelPile[self.fuelBay[0]].paint([left+5,top + 44])
        self.myFuelPile[self.fuelBay[1]].paint([left+5+(173-146),top + 44])
        self.myFuelPile[self.fuelBay[2]].paint([left+5+(200-146),top + 44])
        
        pygame.draw.rect(enviro.screen, THECOLORS["blue"], [left+4,top+71,80,9], 0)
        for i in range(0, self.upgrades):
            pygame.draw.rect(enviro.screen, [130,202,253], [left+6+i*7,top+73,5,5], 0)
        
    def repaint(self):
        enviro.screen.blit(self.image, self.rect)
        
        left = self.rect.left
        top = self.rect.top
        self.myFuelPile[self.fuelBay[0]].paint([left+5,top + 44])
        self.myFuelPile[self.fuelBay[1]].paint([left+5+(173-146),top + 44])
        self.myFuelPile[self.fuelBay[2]].paint([left+5+(200-146),top + 44])
        
        pygame.draw.rect(enviro.screen, THECOLORS["blue"], [left+4,top+71,80,9], 0)
        for i in range(0, self.upgrades):
            pygame.draw.rect(enviro.screen, [130,202,253], [left+6+i*7,top+73,5,5], 0)
            
    def upgrade(self):
        if self.upgrades < 11:
            self.upgrades = self.upgrades + 1
            enviro.laserUpgrades = enviro.laserUpgrades + 1
            self.applyUpgrade()
            self.repaint()
            return True
        return False
    
    def applyUpgrade(self):
        self.laserPower += enviro.LASER_UPGRADE_POWER
        self.aimTime -= 7.5
        #print "Laser power=", self.laserPower, " aimTime=", self.aimTime

        
    def stashStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                self.fuelBay[i] = 10
                self.promises = self.promises - 1
                
                # pretty sure this is too simple, but moving on...
                # "if we're out of gas then this pad got loaded with 9
                #  and the laser is restocked..." -- but what if there's
                #  another bay with fuel? I think we restock too soon?
                if self.consuming == 0:
                    self.fuelBay[i] = 9
                    self.consuming = enviro.LASER_PER_PELLET
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
        
    
    # See if we could use more fuel for laser
    def needFuel(self):
        if enviro.laserRefuelDisabled:
            return False
        
        emptyBays = 0
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                emptyBays += 1
        if emptyBays > self.promises:
            return True
        return False 
    
    # See if we're about to run out of laser power
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
               
    def promiseRefuel(self):
        self.promises = self.promises + 1    

    def autoTarget(self, bombList):
        targetCoord = [0,0]
        
        if self.state == "Armed":
            self.aimCount = self.aimCount + 1
            if self.aimCount > self.aimTime:
                self.aimCount = 0
                self.state = "Shooting"
        elif self.state == "Shooting":
            if len(bombList) > 0:
                
                lowest = 0
                for bomb in bombList:
                    if bomb.rect.top > lowest:
                        lowest = bomb.rect.top
                        targetBomb = bomb
                targetCoord = targetBomb.rect.center
                #print "autoshoot! target=",targetCoord
                
                self.state = "Armed"
            
        return targetCoord
        
        
    def shoot(self, bombList, cursor, mouseButtonUp, autoTargeting):
        stillShooting = False
        laserHitCenter = [0,0]
        shootingBomb = False
        
        # This could be better?
        if mouseButtonUp:
            return False # not shooting anymore

        cost = 5 + self.upgrades * enviro.LASER_COST_FACTOR     
        self.consuming -= cost
        #print "Shooting, power=", enviro.LASER_POWER, "cost=", cost, "consuming buffer=", self.consuming
        
        if self.consuming < 1:
            if self.fuelBay[self.consumingBay] == 0:            
                for i in range(0,3):
                    if self.fuelBay[i] > 0:
                        self.consumingBay = i            
            
            if self.fuelBay[self.consumingBay] > 0:
               self.consuming = enviro.LASER_PER_PELLET
               self.fuelBay[self.consumingBay] = self.fuelBay[self.consumingBay] - 1
               self.repaint()
        
        if self.consuming < 1:
            return False            
        
        target = TargetSprite()
        target.rect.centerx = cursor[0]
        target.rect.centery = cursor[1]        
        
        miss = True
        
        # target the mothership
        if not autoTargeting and enviro.mother.rect.center[0] < 680: # don't target if not fully in area
        
            motherHit = enviro.mother.test(target, "Hit", self.laserPower)
            hit = motherHit[0]
            killed = motherHit[1]
            if motherHit:
                #print "hit the mothership!"
                laserHitCenter = enviro.mother.rect.center            
                if hit and not killed:
                    stillShooting = True
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.MOTHER_SHOT])
                    else:
                        print "no channel for mother shot sound, will try to use main"
                        enviro.soundEffect[Noise.MOTHER_SHOT].play()  
                    miss = False
                elif killed: # killed him
                    stillShooting = False
                    #print "Laser: killed mother!"

                    # Too simple, we might have all channels tied up so no sound:
                    #enviro.soundEffect[Noise.FIGHTER_KILLED].play()
                    # Instead we'll try finding a channel, and force kill on the longest playing if required:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.MOTHER_HIT])
                    else:
                        print "no channel for mother kill sound, will try to use main"
                        enviro.soundEffect[Noise.MOTHER_HIT].play()
                    miss = False

        # target a fighter
        if miss and not autoTargeting:
            fighters = enviro.mother.getFighterFleet()
            for fighter in fighters:
                fighterHit = fighter.test(target, "hit", self.laserPower)
                hit = fighterHit[0]
                killed = fighterHit[1]
                laserHitCenter = fighter.rect.center            
                if hit and not killed:
                    stillShooting = True
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.FIGHTER_HIT])
                    else:
                        print "no channel for fighter shot sound, will try to use main"
                        enviro.soundEffect[Noise.FIGHTER_HIT].play() 
                    miss = False
                    break                
                elif killed: # killed him
                    enviro.mother.notifyDeadFighter(fighter)
                    stillShooting = False
                    #print "Laser: killed fighter!"

                    # Too simple, we might have all channels tied up so no sound:
                    #enviro.soundEffect[Noise.FIGHTER_KILLED].play()
                    # Instead we'll try finding a channel, and force kill on the longest playing if required:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.FIGHTER_KILLED])
                    else:
                        print "no channel for fighter kill sound, will try to use main"
                        enviro.soundEffect[Noise.FIGHTER_KILLED].play()
                    miss = False
                    break        
        
        
        # target a bomb
        if miss:
            shootingBomb = True
            targetHit = False
            if len(bombList) > 0:
                for bomb in bombList:
                    targetHit = bomb.test(target, "hit")
                    if targetHit:
                        laserHitCenter = bomb.rect.center
                        stillShooting = False
                        #enviro.soundEffect[Noise.BOMB_HIT].play()
                        channel = pygame.mixer.find_channel(True)
                        if channel:
                            #print "got channel"
                            channel.play(enviro.soundEffect[Noise.BOMB_HIT])
                        else:
                            print "no channel for mother kill sound, will try to use main"
                            enviro.soundEffect[Noise.BOMB_HIT].play()                         
                        
                        
                        miss = False
                        break
                
        if miss:
            channel = pygame.mixer.find_channel(True)
            if channel:
                #print "got channel"
                channel.play(enviro.soundEffect[Noise.LASER_MISS])
            else:
                print "no channel for mother kill sound, will try to use main"
                enviro.soundEffect[Noise.LASER_MISS].play()            
            
            
            #enviro.soundEffect[Noise.LASER_MISS].play()
            laserHitCenter = cursor
        
        #print "Laser shot to", laserHitCenter
        if shootingBomb:
            pygame.draw.lines(enviro.screen, [255,0,0], False, [[683,448],laserHitCenter], 1)
        else:
            pygame.draw.lines(enviro.screen, [0,255,0], False, [[683,448],laserHitCenter], 3)
        return stillShooting  
    
if __name__ == '__main__':
    
    print "TEST: laser"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
# stuff needed for init:

    for i in range(0,11):
        fuelFile = "fuelStore" + str(i) + ".png"
        fuelState = FuelStuff(fuelFile)
        enviro.fuelPile.append(fuelState)
        
    laserFile = "laser.png"


    l = Laser(laserFile)
    l.paint([640,450], enviro.fuelPile)  
    

            
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (event.type == pygame.KEYDOWN):
            if (pygame.key.get_mods() == 1024): # command key
                if (event.key == 113):   # q
                    sys.exit()
            if event.key == pygame.K_SPACE:                    
                l.upgrade()

                   
                    
        myClock.tick(30)
        pygame.display.flip()       
          