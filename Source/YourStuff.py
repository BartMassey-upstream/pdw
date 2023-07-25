# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import random
import os
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise
    
from AttackerStuff import ShieldSprite
from Harvester import Harvester
from Generator import Generator


class TargetSprite(pygame.sprite.Sprite):
    def __init__(self, location = [0,0]):
        
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([24,24])
        image_surface.fill([0,0,255])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
  
class Shop(pygame.sprite.Sprite):
    def __init__(self, image_file, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = 9
        self.rect.left = x
        self.rect.top = y
        self.isPainted = False
        
    def paintPad(self):
        pass        
        
    def paint(self):
        enviro.screen.blit(self.image, self.rect)
        self.isPainted = True
       
     
class BotFactory(pygame.sprite.Sprite):
    def __init__(self, image_file, left, top, needStuff0_img, needMoney0_img, needMoney1_img, needMoney2_img, needStuff_img, built_img):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top 
        self.location = 0
        
        self.need0_white = pygame.image.load(os.path.join(enviro.artPathHack,needStuff0_img))
        self.need0 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney0_img))
        self.need1 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney1_img))
        self.need2 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney2_img))
        self.needStuffToBuild = pygame.image.load(os.path.join(enviro.artPathHack,needStuff_img))
        self.botFactoryBuilt = pygame.image.load(os.path.join(enviro.artPathHack,built_img)).convert_alpha()
        self.needCount = 0
        self.needXOffset = 20
        self.needYOffset = 60        
        self.needType = "none"         
        self.built = 0
        self.padPainted = False
        
    def paintPad(self):
        enviro.screen.blit(self.image, self.rect)
        self.padPainted = True        
        
    def build(self):
        self.built = 1
        enviro.botFactoryIsBuilt = True
        enviro.screen.blit(self.botFactoryBuilt, self.rect)
        
        coordX = enviro.getLocationX(0)
        coordY = enviro.getLocationY(0)
        for i in range(10):
            pygame.draw.rect(enviro.screen, [255,0,0], 
                [(coordX + 5) + (i+1) * 7,(coordY + 20),5,2],0)
        
    def needMoney(self):
        #print "NEED MONEY"
        paintX = self.rect.left
        paintY = self.rect.top
        enviro.screen.blit(self.need1, [paintX+self.needXOffset, paintY+self.needYOffset])
        self.needType = "credits"
        self.needCount = 100
        
    def needStuff(self):
        #print "NEED STUFF"
        paintX = self.rect.left
        paintY = self.rect.top
        self.needType = "stuff"
        enviro.screen.blit(self.needStuffToBuild, [paintX+self.needXOffset, paintY+self.needYOffset])
        self.needCount = 100
        
    def clearNeeds(self):

        paintX = self.rect.left
        paintY = self.rect.top
        if self.needCount > 0:
            self.needCount = self.needCount - 1
            #print "factory need type:", self.needType, " count:", self.needCount
            if self.needCount == 0:
                if self.built == 0:
                   enviro.screen.blit(self.need0, [paintX+self.needXOffset, paintY+self.needYOffset])
                else:
                   enviro.screen.blit(self.need0_white, [paintX+self.needXOffset, paintY+self.needYOffset])
            else:
                needPhase = self.needCount / 10 - 1
                if needPhase % 2 == 1 and needPhase > 1:
                    enviro.screen.blit(self.need2, [paintX+self.needXOffset, paintY+self.needYOffset])
                else:
                    if self.needType == "credits":
                        enviro.screen.blit(self.need1, [paintX+self.needXOffset, paintY+self.needYOffset])
                    elif self.needType == "stuff":
                        enviro.screen.blit(self.needStuffToBuild, [paintX+self.needXOffset, paintY+self.needYOffset])                
        
    def paint(self,fuelPile):
        enviro.screen.blit(self.image, self.rect)
        self.myFuelPile = fuelPile

        self.myFuelPile[self.fuelBay[1]].paint([146,150])
        self.myFuelPile[self.fuelBay[0]].paint([173,150])
        self.myFuelPile[self.fuelBay[2]].paint([200,150])
        
    def repaintBays(self):
        #enviro.screen.blit(self.image, self.rect)

        self.myFuelPile[self.fuelBay[1]].paint([146,150])
        self.myFuelPile[self.fuelBay[0]].paint([173,150])
        self.myFuelPile[self.fuelBay[2]].paint([200,150])
    
    def stashStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                self.fuelBay[i] = 10
                self.repaintBays()
                return True
        return False
    
    def getStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] == 10:
                self.fuelBay[i] = 0
                self.repaintBays()
                return True
        return False
            
        
class Base(pygame.sprite.Sprite):
    def __init__(self, image_file, left, top):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top 
        self.location = 4 

        self.fuelBay = [0,0,0]
        
    def paintPad(self):        
        pass
        
    def clearNeeds(self):
        pass
        
    def isFull(self):
        for i in range(0,3):
            if self.fuelBay[i] <> 10:
                return False
        return True
    
    def hasStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] > 0:
                return True
        return False
        
    def paint(self,fuelPile):
        enviro.screen.blit(self.image, self.rect)
        self.myFuelPile = fuelPile

        self.myFuelPile[self.fuelBay[1]].paint([146,175])
        self.myFuelPile[self.fuelBay[0]].paint([173,175])
        self.myFuelPile[self.fuelBay[2]].paint([200,175])
        
    def repaintBays(self):
        #enviro.screen.blit(self.image, self.rect)

        self.myFuelPile[self.fuelBay[1]].paint([146,175])
        self.myFuelPile[self.fuelBay[0]].paint([173,175])
        self.myFuelPile[self.fuelBay[2]].paint([200,175])
    
    def stashStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] == 0:
                self.fuelBay[i] = 10
                self.repaintBays()
                return True
        return False
    
    def getStuff(self):
        for i in range(0,3):
            if self.fuelBay[i] == 10:
                self.fuelBay[i] = 0
                self.repaintBays()
                return True
        return False
            

        
class FuelStuff(pygame.sprite.Sprite):
    def __init__(self, image_file):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        
    def paint(self, location):
        self.rect.left = location[0]
        self.rect.top = location[1]
        
        enviro.screen.blit(self.image, self.rect)

           


class GasGauge(pygame.sprite.Sprite):
    def __init__(self, image_file):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage))
        self.rect = self.image.get_rect()
        
    def paint(self, location):
        self.rect.left = location[0]
        self.rect.top = location[1]
        
        enviro.screen.blit(self.image, self.rect)


    
class Pad(pygame.sprite.Sprite):
    def __init__(self, location, image_file, left, top, needMoney0_img, needMoney1_img, needMoney2_img, needStuff_img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,image_file)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.location = location
        
        self.need0 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney0_img)).convert_alpha()
        self.need1 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney1_img)).convert_alpha()
        self.need2 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney2_img)).convert_alpha()
        self.needStuffToBuild = pygame.image.load(os.path.join(enviro.artPathHack,needStuff_img)).convert_alpha()
        self.needCount = 0
        self.needType = "none"
        self.padPainted = False
        
    def paintPad(self):
        enviro.screen.blit(self.image, self.rect)
        self.padPainted = True        
        
    def needMoney(self):
        paintX = self.rect.left
        paintY = self.rect.top
        enviro.screen.blit(self.need1, [paintX, paintY])
        self.needType = "credits"
        self.needCount = 100
        
    def needStuff(self):
        paintX = self.rect.left
        paintY = self.rect.top
        self.needType = "stuff"
        #enviro.screen.blit(self.needStuffToBuild, [paintX+9, paintY+62, 75, 23])
        enviro.screen.blit(self.needStuffToBuild, [paintX, paintY])
        self.needCount = 100
                
    def clearNeeds(self):
        paintX = self.rect.left
        paintY = self.rect.top
         
        if self.needCount > 0:
            pygame.draw.rect(enviro.screen, [0,0,0],[paintX,paintY,90,90])
            self.needCount = self.needCount - 1
            if self.needCount == 0:
                enviro.screen.blit(self.need0, [paintX, paintY])
            else:
                needPhase = self.needCount / 10 - 1
                if needPhase % 2 == 1 and needPhase > 1:
                    enviro.screen.blit(self.need2, [paintX, paintY])
                else:
                    if self.needType == "credits":
                        enviro.screen.blit(self.need1, [paintX, paintY])
                    else:
                        enviro.screen.blit(self.needStuffToBuild, [paintX, paintY])                

                
        
        
class You(pygame.sprite.Sprite):
    def __init__(self, image_file_idle, image_file_carrying_stuff, img_carrying_gas, speed):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file_idle
        self.theImageCarrying = image_file_carrying_stuff
        self.theImageCarryingGas = img_carrying_gas
        self.image_empty = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.image_carrying_stuff = pygame.image.load(os.path.join(enviro.artPathHack,self.theImageCarrying)).convert_alpha()
        self.image_carrying_gas = pygame.image.load(os.path.join(enviro.artPathHack,self.theImageCarryingGas)).convert_alpha()
        
        self.image = self.image_empty
        self.rect = self.image.get_rect()
        
        self.goalX = 3
        self.goalY = 1
        self.locationX = self.getMapX(self.goalX,self.goalY)
        self.locationY = self.getMapY(self.goalX,self.goalY)
        
        self.rect.left = self.locationX
        self.rect.top = self.locationY
        self.speed = speed
        
        self.buffer = []
        self.carrying = 0
        
        
    def bufferIt(self, direction):
        if direction == "clear":
            self.buffer = []
            return
        # This was great, but I'd need to display buffered strokes
        #self.buffer.append(direction)
        # instead:
        self.buffer = []
        self.buffer.append(direction)

    def aimLeft(self, pads):
        #print "aim left"
        if self.speed[0] <> 0 or self.speed[1] <> 0:
            self.bufferIt("left")
            return        
        
        newSpeed  = [enviro.YOURSPEED * -1,0]
        if enviro.testCollision(self, newSpeed, pads):
            return
        
        if self.goalX > 0:
            testX = self.getMapX(self.goalX - 1, self.goalY)
            if testX <> -1:
                self.goalX = self.goalX - 1
                self.speed = newSpeed
##            else:
##                print "off"
##        else:
##            print "edge"

##        if (self.goalX > 0):
##            self.goalX = self.goalX - 1
##            self.speed = newSpeed
        
    def aimRight(self,pads):
#        if self.speed[0] < 0:
#            self.bufferIt("clear")
        if self.speed[0] <> 0 or self.speed[1] <> 0:
            self.bufferIt("right")
            return
        
        newSpeed  = [enviro.YOURSPEED,0]
        if enviro.testCollision(self, newSpeed, pads):
            return
        
        testX = self.getMapX(self.goalX + 1, self.goalY)
        if testX <> -1:
            self.goalX = self.goalX + 1
            self.speed = newSpeed
##        else:
##            print "off"
                        
    def aimUp(self, pads):
        if self.speed[0] <> 0 or self.speed[1] <> 0:
            self.bufferIt("up")
            return
        if (self.goalY == 0):
            #print "edge"
            return
        newSpeed  = [0, enviro.YOURSPEED * -1]
        if enviro.testCollision(self, newSpeed, pads):
#            self.bufferIt('up')
#            print "Buffered up"
            return
        
        self.goalY = self.goalY - 1
        self.speed = newSpeed
    
    def aimDown(self, pads):
        if self.speed[0] <> 0 or self.speed[1] <> 0:
            self.bufferIt("down")
            return        
        
        newSpeed  = [0, enviro.YOURSPEED]
        if enviro.testCollision(self, newSpeed, pads):
            return
            
        testY = self.getMapY(self.goalX, self.goalY + 1)
        if testY <> -1:
            self.goalY = self.goalY + 1
            self.speed = newSpeed
        
    def moveYou(self, pads):
        goalX = self.getMapX(self.goalX,self.goalY)
        goalY = self.getMapY(self.goalX,self.goalY)
        
#        print "GoalX",goalX,"GoalY",goalY,"SpeedX",you.speed[0],"SpeedY",you.speed[1]
        #print "BUFFER", you.buffer
            
        youX = enviro.you.rect.left
        youY = enviro.you.rect.top
        
        if enviro.you.speed[0] < 0:
            if youX + enviro.you.speed[0] < goalX:
                enviro.you.speed[0] = goalX - youX
        if enviro.you.speed[0] > 0:
            if youX + enviro.you.speed[0] > goalX:
                enviro.you.speed[0] = goalX - youX
        if enviro.you.speed[1] < 0:
            if youY + enviro.you.speed[1] < goalY:
                enviro.you.speed[1] = goalY - youY
        if enviro.you.speed[1] > 0:
            if youY + enviro.you.speed[1] > goalY:
                enviro.you.speed[1] = goalY - youY
                
# wow this was awful, even for me!                
##        if self.carrying == 1:
##            self.image = pygame.image.load(self.theImageCarrying)
##        elif self.carrying == 2:
##            self.image = pygame.image.load(self.theImageCarryingGas)
##        else:
##            self.image = pygame.image.load(self.theImage)

        if self.carrying == 1:
            self.image = self.image_carrying_stuff
        elif self.carrying == 2:
            self.image = self.image_carrying_gas
        else:
            self.image = self.image_empty         
            
        # This worked perfectly, except when the bots collided with you...
        # so now we'll draw the road each time.
        #enviro.screen.blit(enviro.roadImage,self.rect,self.rect)
        self.rect = self.rect.move(self.speed)
        enviro.screen.blit(self.image, self.rect)
        #print self.rect.top, self.rect.left 
        #pygame.draw.rect(enviro.screen, [255,255,0], self.rect, 0)
              
                
        if youX == goalX and youY == goalY:
            enviro.you.speed = [0,0]

            if len(enviro.you.buffer) > 0:
                next = enviro.you.buffer.pop(0)
                return next

    def interact(self, generators, shields, base, laser):
        action = [-1,1]
        if self.speed[0] <> 0 or self.speed[1] <> 0:
            #print "Buffering action"
            self.bufferIt("act")
            return action
        #print "ACT! at goalX", self.goalX, "goalY", self.goalY
        
        if self.goalX == 5 and self.goalY == 2:
            action[1] = 0
            action[0] = 0
            #print "At the gas factory!"
            if enviro.gasFactory.built == 0 and enviro.gasFactory.padPainted:
                #print "not built"
                
                if enviro.NEED_MONEY_TO_BUILD and not enviro.credits > 999:
                    #print "Need 1000 for factory, you only have ", enviro.credits
                    enviro.gasFactory.needMoney()
                else:
                    if self.carrying == 0:
                       #print "Gotta have stuff to make it"
                       enviro.gasFactory.needStuff()
                    else:
                        #print "build the factory!"
                        enviro.gasFactory.build()
                        self.carrying = 0
                        if enviro.NEED_MONEY_TO_BUILD:
                            enviro.credits = enviro.credits - 1000
                            enviro.writeCredits(enviro.credits)
            else:
                if enviro.gasFactory.padPainted:
                    #print "Gas factory built, produce gas with stuff!"
                    if self.carrying == 0:
                        #print "need stuff to make gas!"
                        enviro.gasFactory.needStuff()
                    else:
                        if self.carrying == 1:
                            self.carrying = 2                
        
        elif self.goalX == 1 and self.goalY == 0 and enviro.factory.padPainted:
            action[1] = 0
            action[0] = 0
            #print "At bot factory"
            if enviro.factory.built == 0:
                if enviro.NEED_MONEY_TO_BUILD and enviro.credits < 1000:
                    #print "Need 1000 for factory, you only have ", enviro.credits
                    enviro.factory.needMoney()
                else:
                    if self.carrying <> 1:
                       #print "Gotta have stuff to make it"
                       enviro.factory.needStuff()
                    else:
                        #print "build the factory!"
                        enviro.factory.build()
                        self.carrying = 0
                        if enviro.NEED_MONEY_TO_BUILD:
                            enviro.credits = enviro.credits - 1000
                            enviro.writeCredits(enviro.credits)
                        
            else:
                #print "built, make a bot?"
                if enviro.NEED_MONEY_TO_BUILD and not enviro.credits > 999:
                    #print "Need 1000 for factory, you only have ", enviro.credits
                    enviro.factory.needMoney()
                elif self.carrying == 0 or self.carrying == 2:
                    #print "need stuff to make a bot!"
                    enviro.factory.needStuff()
                else:
                    if len(enviro.harvesters) < 10:
                        #print "BUILD BOT"
                        self.carrying = 0
                        if enviro.NEED_MONEY_TO_BUILD:
                            enviro.credits = enviro.credits - 1000
                            enviro.writeCredits(enviro.credits)
                        #print "You bought a harvester!"
                        newHarv = Harvester(len(enviro.harvesters))
                        enviro.harvesters.append(newHarv)
                        harvCount = len(enviro.harvesters)
                        #print "Now have", harvCount, "harvesters"
                        
                        coordX = enviro.getLocationX(0)
                        coordY = enviro.getLocationY(0)
                        pygame.draw.rect(enviro.screen, [255,255,255], 
                            [(coordX + 5) + (harvCount) * 7,(coordY + 20),5,5],0)                        
                        
                        
                    #else:
                        #print "Max 10 harvesters!"
                        
        if self.goalX == 3 and self.goalY == 0:
            action[0] = 1
        if self.goalX == 5 and self.goalY == 0:
            action[0] = 2
        if self.goalX == 1 and self.goalY == 1:
            action[0] = 3
        if self.goalX == 3 and self.goalY == 1:
            action[1] = 0
            action[0] = 4
            if self.carrying == 1:
                #print "at home and carrying stuff, drop it"
                if base.stashStuff():
                    self.carrying = 0
            else:
                if self.carrying == 0:
                    #print "at base and not carrying"                    
                    if base.getStuff():
                        self.carrying = 1
                #else:
                    #print "gas at home? HMM"
        if self.goalX == 5 and self.goalY == 1:
            action[0] = 5
        if self.goalX == 1 and self.goalY == 2:
            action[0] = 6
        if self.goalX == 3 and self.goalY == 2:
            action[0] = 7
        if self.goalX == 5 and self.goalY == 2:
            action[0] = 8
            
        if self.goalX == 8 and self.goalY == 3 and enviro.combatStarted: # the shield station
            if self.carrying == 1:
                if shields.loadFuel():
                    self.carrying = 0
            elif self.carrying == 2:
                if shields.upgrade():
                    self.carrying = 0
            elif self.carrying == 0:
                if shields.unloadStuff():
                    self.carrying = 1                    
                    
        if self.goalX == 9 and self.goalY == 3 and enviro.combatStarted: # the laser station
            if self.carrying == 2:
                if laser.upgrade():
                    self.carrying = 0
            elif self.carrying == 1:
                if laser.stashStuff():
                    self.carrying = 0
            elif self.carrying == 0:
                if laser.unloadStuff():
                    self.carrying = 1
                    
        if self.goalX == 7 and self.goalY == 3 and enviro.shop.isPainted == True: # the shop
            if self.carrying == 1:
                self.carrying = 0
                enviro.credits = enviro.credits + 1000
                #print "now you have ", enviro.credits
                enviro.writeCredits(enviro.credits)
##            else:
##                if self.carrying == 2:
##                    print "gas at market, hmm"
                    
        return action
    
    def getMapX(self, mapLocX, mapLocY):
        if mapLocX > len(enviro.map[mapLocY]) - 1:
            return -1
        if enviro.map[mapLocY][mapLocX][0] < 0:
            return -1
        return enviro.map[mapLocY][mapLocX][0]

    def getMapY(self, mapLocX, mapLocY):
        if mapLocY > len(enviro.map) - 1:
            return -1
        if enviro.map[mapLocY][mapLocX][1] < 0:
            return -1
        return enviro.map[mapLocY][mapLocX][1]
