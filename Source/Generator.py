# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame, random
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise

from YourStuff import *

class Generator:
    def __init__(self, location, gauges, image_file):
        
        self.location = location
        self.isReady = False
        self.isTargeted = False
        self.processCount = 0
        self.cycleCount = 0
        self.gas = 60
        self.gasPromised = False
                
        coordX = enviro.getLocationX(location)
        coordY = enviro.getLocationY(location)
        
        image = pygame.image.load(os.path.join(enviro.artPathHack,image_file)).convert_alpha()
        enviro.screen.blit(image,[coordX,coordY])
        
        #pygame.draw.rect(enviro.screen, [0,0,200], [coordX+5,coordY+5,80,80],0) # generator
        #pygame.draw.rect(enviro.screen, THECOLORS["gray63"], [coordX+25,coordY+20,40,40],0) # result box
        gauges[0].paint([coordX+15,coordY+10])
        
        self.genImage = []
        for i in range (1,11):
            genImg = pygame.image.load(os.path.join(enviro.artPathHack,"generating-"+str(i)+".png")).convert_alpha()
            self.genImage.append(genImg)
            
        
    def __str__(self):
        msg = "GENERATOR DEBUGGER:" + "\n"
        msg += " Location: " + str(self.location) + "\n"
        msg += " Ready: " + str(self.isReady) + "\n"
        msg += " Targeted: " + str(self.isTargeted) + "\n"
        msg += " Process count: "  + str(self.processCount) + "\n"
        return msg
    
    def checkTankEmpty(self):
        if self.gas == 0 and self.gasPromised == False:
            return True
        return False
                
    def produce(self, gauges):

        coordX = enviro.getLocationX(self.location)
        coordY = enviro.getLocationY(self.location)
                
        if (self.processCount == 10):
            self.isReady = True
            self.processCount = 0
            pygame.draw.rect(enviro.screen, [0,255,0], 
               [(coordX + 30), (coordY + 25),30,30],0) # the result
    
        hasGas = False
        if (self.isReady == False):
            if self.cycleCount == 0 and self.processCount == 0:
                if self.gas > 0:
                    self.gas = self.gas - 20
                    hasGas = True
                
                    if self.gas == 40:
                        gauges[1].paint([coordX+15,coordY+10])
                    if self.gas == 20:
                        gauges[2].paint([coordX+15,coordY+10])
                    if self.gas == 0:
                        gauges[3].paint([coordX+15,coordY+10])
            else:
                hasGas = True
                
            if hasGas:
                self.cycleCount = self.cycleCount + 1
                if self.cycleCount > enviro.PRODUCTION_TIMER:
                    self.cycleCount = 0
                    self.processCount = self.processCount + 1
                    enviro.screen.blit(self.genImage[self.processCount-1], [coordX+5,coordY+15])
##                    pygame.draw.rect(enviro.screen, [255,255,0], 
##                        [(coordX + 4) + self.processCount * 7,(coordY + 70),5,5],0)
                        
    def refill(self, gasGauges):
        coordX = enviro.getLocationX(self.location)
        coordY = enviro.getLocationY(self.location)
                
        self.gas = 60
        gasGauges[0].paint([coordX+15,coordY+10])
        self.gasPromised = False
                    
    def harvestStuff(self):
        if self.isReady == True:
            self.isReady = False
            self.isTargeted = False
            self.processCount = 0
            self.cycleCount = 0
            coordX = enviro.getLocationX( self.location )
            coordY = enviro.getLocationY( self.location )
            #pygame.draw.rect(enviro.screen, [100,100,0], [coordX+25,coordY+10,40,40],0) # result box
            pygame.draw.rect(enviro.screen, [0,0,200], 
                        [ coordX + 5, coordY + 70,80,5],0) # clear the progress meter
            pygame.draw.rect(enviro.screen, [0,0,200], 
                   [(coordX + 30), (coordY + 25),30,30],0) # the result
            return True
        return False
    
    
if __name__ == '__main__':
    
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
        
    
# stuff needed for init:
    gasFiles = ["gas-full.png", "gas-twoThirds.png", "gas-oneThird.png", "gas-empty.png"]
    for gasFile in gasFiles:
        gas = GasGauge(gasFile)
        enviro.gasGauges.append(gas)


    newGen = Generator(5,enviro.gasGauges, "generator0.png")
    newGen.refill(enviro.gasGauges)
    
    enviro.PRODUCTION_TIMER = 1
            
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                        
                if event.key == pygame.K_SPACE:
                    print "Generate!"
                    newGen.produce(enviro.gasGauges)
                   
                    
        myClock.tick(30)
        pygame.display.flip()       
              