# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame, random
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise

import sys    # for testing
import os
    
from AttackerStuff import ShieldSprite

class Harvester:
    def __init__(self, count):
        
        self.imageEmpty = pygame.image.load(os.path.join(enviro.artPathHack,"botEmpty.png")).convert_alpha()
        self.imageStuff = pygame.image.load(os.path.join(enviro.artPathHack,"botWithStuff.png")).convert_alpha()
        self.imageGas = pygame.image.load(os.path.join(enviro.artPathHack,"botWithGas.png")).convert_alpha()
        self.rect = self.imageEmpty.get_rect()
        
        self.state = "Returning" # they used to start Idle, now "return" to home
        self.target = 0 # we're on the path to location 0
        self.progress = 3 # was 0
        self.fleetPosition = count
        self.cooldown = 0
        self.gasTarget = -1

        self.locationX = 35
        self.locationY = 100
        pygame.draw.rect(enviro.screen, [200,0,0], [self.locationX,self.locationY,40,40], 0)
        
    def __str__(self):
##        msg = "HARVESTER DEBUGGER:" + "\n"
        msg = " Harvester: " + str(self.fleetPosition) + "\n"
        msg += " State: " + str(self.state) + "\n"
        msg += " Location: " + str(self.locationX) + "," + str(self.locationY) + "\n"
        msg += " Progress: " + str(self.progress)
        return msg        
                    
    def spawn(self):
        # home location
        self.locationX = 165
        self.locationY = 230
        
        coordX = enviro.getLocationX(4)
        coordY = enviro.getLocationY(4)
        pygame.draw.rect(enviro.screen, [255,255,255], 
            [(coordX + 5) + (self.fleetPosition+1) * 7,(coordY + 70),5,5],0)
            
        enviro.screen.blit(self.imageEmpty, [self.locationX,self.locationY])

    def move(self, goalX, goalY, pathDirection):
        #print "Target=", self.target, "progress=", self.progress
        
        # erase where we're at now -- or not, since in the end I decided to paint the road every frame
        #pygame.draw.rect(enviro.screen, [0,0,0], [self.locationX,self.locationY,40,40], 0)
        #self.rect.top = self.locationY
        #self.rect.left = self.locationX
        #enviro.screen.blit(enviro.roadImage,self.rect,self.rect)
        
        # then move, like add 1 to y
        if self.locationY < goalY:
            self.locationY = self.locationY + enviro.SPEED
            if self.locationY > goalY:
                self.locationY = goalY
        if self.locationY > goalY:
            self.locationY = self.locationY - enviro.SPEED
            if self.locationY < goalY:
                self.locationY = goalY
        if self.locationX < goalX:
            self.locationX = self.locationX + enviro.SPEED
            if self.locationX > goalX:
                self.locationX = goalX
        if self.locationX > goalX:
            self.locationX = self.locationX - enviro.SPEED
            if self.locationX < goalX:
                self.locationX = goalX
        
        # draw new
        if self.state == "GotGas" or self.state == "DeliverGas":
           enviro.screen.blit(self.imageGas, [self.locationX,self.locationY])            
        elif (self.state == "Carrying" or
            self.state == "Selling" or 
            self.state == "Fueling" or 
            self.state == "Stuck" or 
            self.state == "Reenergizing" or
            self.state == "GetGas"):
           self.paintHarvesterWithStuff()
        else:
           enviro.screen.blit(self.imageEmpty, [self.locationX,self.locationY])
        
        if self.locationX == goalX and self.locationY == goalY:
            if pathDirection == 1:
                self.progress = self.progress + 1
            else:
                self.progress = self.progress - 1
        return self.progress
    
    def paintHarvesterWithStuff(self):
        #pygame.draw.rect(enviro.screen, [0,255,0], 
        #       [(self.locationX + 5), (self.locationY + 5),30,30],0)
        enviro.screen.blit(self.imageStuff, [self.locationX,self.locationY])            
            
    def home(self):
        # erase from playfield
        #pygame.draw.rect(enviro.screen, [0,0,0], [self.locationX,self.locationY,40,40], 0)
        self.rect.top = self.locationY
        self.rect.left = self.locationX
        #enviro.screen.blit(enviro.roadImage,self.rect,self.rect)        
        
        # add back to home list
        coordX = enviro.getLocationX(4)
        coordY = enviro.getLocationY(4)
    
        pygame.draw.rect(enviro.screen, [255,0,0], 
            [(coordX + 5) + (self.fleetPosition+1) * 7,(coordY + 70),5,5],0)

    def getNextState(self, shields, base, generators, laser):
        #print "state ", self.state, "progress", self.progress, "x", self.locationX
        
        if self.state == "Cooling":
            self.cooldown = self.cooldown - 1
            if self.cooldown < 1:
                self.state = "Idle"
                
        # A new "first priority" (sigh), can't let all production die!
        allAreEmpty = False
        if self.state == "Idle" and enviro.gasFactory.built == 1:
            allAreEmpty = True
            for generator in generators:
                if not generator.checkTankEmpty():
                    allAreEmpty = False
        
        # First priority is to capitalize on when she's dead, sell
        if self.state == "Idle" and base.isFull():
            if enviro.mother.state == "Hit" or enviro.mother.state == "Waiting":
                if enviro.combatStarted:
                    if base.getStuff():
                        self.state = "Selling"
                        self.target = 13 # the market
                        self.progress = 0
                        self.spawn() 
                        
        # Under combat, don't let the shields or laser run dry...
        # but they don't need to be chock full either, not if we've got
        # a generator out of gas
        if (self.state == "Idle" or self.state == "Stuck") and not allAreEmpty:
            # Be sure we can blast away at our attackers
            if laser.nearlyEmpty():
                if base.getStuff():
                    self.state = "Reenergizing"
                    laser.promiseRefuel()
                    self.target = 10
                    self.progress = 0
                    self.spawn()
            # ...and be sure to keep a roof over our head
            elif shields.nearlyEmpty():
                if base.getStuff():
                    self.state = "Fueling"
                    shields.promiseRefuel()
                    self.target = 9 # the shield generator
                    self.progress = 0
                    self.spawn()
                        
        # They're not running dry, so next priority is to keep the generators fueled up
        if self.state == "Idle" and enviro.gasFactory.built == 1:
            for generator in generators:
                genIsEmpty = generator.checkTankEmpty()
                if genIsEmpty:
                    #print "Found empty tank"
                    if base.getStuff():
                        generator.gasPromised = True                    
                        self.state = "GetGas"
                        self.target = 8
                        self.gasTarget = generator.location
                        self.progress = 0
                        self.spawn()                       
                        break                                          
        
        if self.state == "Idle":
            # Be sure the shields are pumping safety above our head
            if shields.needFuel():
                if base.getStuff():
                    self.state = "Fueling"
                    shields.promiseRefuel()
                    self.target = 9 # the shield generator
                    self.progress = 0
                    self.spawn()
            # ...and then be sure we're blasting anything we can
            elif laser.needFuel():
                if base.getStuff():
                    self.state = "Reenergizing"
                    laser.promiseRefuel()
                    self.target = 10
                    self.progress = 0
                    self.spawn()
                    
            # Find a generator that has stuff ready to collect...
            for generator in generators:
                # need to check idle here again because two generators could be ready at the same time...
                if self.state == "Idle" and generator.isReady == True and generator.isTargeted == False:
                    #print "Found target to harvest"
                    self.state = "Harvesting"
                    self.target = generator.location
                    generator.isTargeted = True
                    self.progress = 0
                    self.spawn()

        if self.state == "Fueling" or self.state == "Selling":
            goalX = enviro.path[self.target][self.progress][0]
            goalY = enviro.path[self.target][self.progress][1]
            if goalX <> -1:
                self.move(goalX, goalY, 1)
            else:
                if self.state == "Fueling":
                    if shields.loadFuel():
                        self.state = "Returning"
                        self.progress = self.progress - 1;
                    else: # couldn't refuel, must return
                        self.state = "Carrying"
                        self.progress = self.progress - 1;
                elif self.state == "Selling":
                    #print "At market!"
                    enviro.credits = enviro.credits + 1000
                    #print "now you have ", enviro.credits
                    enviro.writeCredits(enviro.credits)
                    self.state = "Returning"
                    self.progress = self.progress - 1
                    enviro.SPEED = enviro.SPEED + .25
                    enviro.YOURSPEED = enviro.YOURSPEED + .25
                    enviro.PRODUCTION_TIMER -= 1
                    if enviro.PRODUCTION_TIMER < 1:
                        enviro.PRODUCTION_TIMER = 1
                    
        if self.state == "Reenergizing":
            goalX = enviro.path[self.target][self.progress][0]
            goalY = enviro.path[self.target][self.progress][1]
            if goalX <> -1:
                self.move(goalX, goalY, 1)
            else:
                if laser.stashStuff():
                    self.state = "Returning"
                    self.progress = self.progress - 1;
                else: # couldn't refuel, must return
                    self.state = "Carrying"
                    self.progress = self.progress - 1; 
                    
        if self.state == "GetGas" or self.state == "DeliverGas":
            goalX = enviro.path[self.target][self.progress][0]
            goalY = enviro.path[self.target][self.progress][1]
            if goalX <> -1:
                self.move(goalX, goalY, 1)
            else:
                if self.state == "GetGas":
                    self.state = "GotGas"
                    self.progress = self.progress - 1;            
                elif self.state == "DeliverGas":
                    #print "At gas target!"
                    for generator in generators:
                        if generator.location == self.target:
                            generator.refill(enviro.gasGauges)
                            break
                    self.state = "Returning"
                    self.progress = self.progress - 1;
            
        if self.state == "Harvesting":
            goalX = enviro.path[self.target][self.progress][0]
            goalY = enviro.path[self.target][self.progress][1]
            
            if goalX <> -1:
                self.move(goalX, goalY, 1)
            else:
                for generator in generators:
                    if self.target == generator.location:
                        if generator.harvestStuff():
                            self.state = "Carrying"
                            self.paintHarvesterWithStuff()
                            self.progress = self.progress - 1;
                        else: # somebody beat me to it
                            self.state = "Returning"
                            self.progress = self.progress - 1

        # Come back, on path direction negative
        if (self.state == "Carrying" or 
            self.state == "Returning" or 
            self.state == "GotGas"):
            goalX = enviro.path[self.target][self.progress][0]
            goalY = enviro.path[self.target][self.progress][1]
            newProgress = self.move(goalX, goalY, -1) 
            if newProgress == -1: # made it home
                if self.state == "Carrying":
                    if base.stashStuff():
                       self.state = "Cooling"
                       self.cooldown = enviro.HARVESTER_COOLDOWN
                       #print "Home!"
                       self.home()
                    else:
                       self.state = "Stuck"
                       self.progress = 0
                       self.target = random.randint(11,12)
                elif self.state == "Returning":
                    self.state = "Cooling"
                    self.cooldown = enviro.HARVESTER_COOLDOWN
                    #print "Home!"
                    self.home()
                elif self.state == "GotGas":
                    self.state = "DeliverGas"
                    self.progress = 0
                    self.target = self.gasTarget
                    
                    
        if self.state == "Stuck":
            if enviro.mother.state == "Hit" or enviro.mother.state == "Waiting":
                if enviro.combatStarted:                
                    self.state = "Selling"
                    self.target = 13 # the market
                    self.progress = 0
                            
            if shields.needFuel():
                self.state = "Fueling"
                self.target = 9 # the shield generator
                self.progress = 0
                shields.promiseRefuel()
                
            elif laser.needFuel():
                self.state = "Reenergizing"
                laser.promiseRefuel()                
                self.target = 10
                self.progress = 0
                
            else:
                # see if the stuff should be made into gas
                genNeedsGas = False
                for generator in generators:
                    genIsEmpty = generator.checkTankEmpty()
                    if genIsEmpty:
                        genNeedsGas = True
                        generator.gasPromised = True                    
                        self.state = "GetGas"
                        self.target = 8
                        self.gasTarget = generator.location
                        self.progress = 0
                        break
                        
                if not genNeedsGas:
                    # we're just stuck, pace awhile and try again in a bit
                    goalX = enviro.path[self.target][self.progress][0]
                    goalY = enviro.path[self.target][self.progress][1]
                    if goalX <> -1:
                        self.move(goalX, goalY, 1)
                    else:
                        self.state = "Carrying"
                        self.progress = self.progress - 1
                        # Huh, I needed to move here to avoid some mean flicker
                        # Not sure why just here though, odd?
                        goalX = enviro.path[self.target][self.progress][0]
                        goalY = enviro.path[self.target][self.progress][1]                        
                        self.move(goalX, goalY, -1) 


if __name__ == '__main__':

    
    print "TEST: Harvester"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])    
    h = Harvester(0)

    pygame.display.flip()
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (event.type == pygame.KEYDOWN):
            if (pygame.key.get_mods() == 1024): # command key
                if (event.key == 113):   # q
                    sys.exit()                    