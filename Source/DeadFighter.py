# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import os
import sys # for testing
from pygame.color import THECOLORS

import enviro # my global game environment
from FloatingSprite import FloatingSprite
from Fighter import Fighter # for testing...

class DeadFighter:
    def __init__(self, filenamePrefix):
        self.deathImage = []
        self.deathFrameCount = 0
        self.top = 0
        self.left = 0
        
        for i in range (1,9):
            deathFile = filenamePrefix + str(i) + ".png"
            deathImage = pygame.image.load(os.path.join(enviro.artPathHack,deathFile)).convert_alpha()
            self.deathImage.append(deathImage)
            
    def __str__(self):
        msg =  "  Dead fighter X:" + str(self.top) + " Y:" + str(self.left)
        msg += "    frameCount=" + str(self.deathFrameCount)
        return msg               
            
    def paint(self):
        #deathFrame = self.deathFrameCount / 10
        deathFrame = self.deathFrameCount
        # maybe we got called too many times... if so, let's not crash
        if deathFrame >= len(self.deathImage):
            return True
        enviro.screen.blit(self.deathImage[deathFrame], [self.top, self.left])
        self.deathFrameCount += 1
        #nextFrame = self.deathFrameCount / 10
        nextFrame = self.deathFrameCount
        # the intention is to signal when we're done, and shouldn't be called again...
        if nextFrame >= len(self.deathImage):
            return True
        return False
    
    def setLocation(self,fighterTop, fighterLeft):
        self.top = fighterTop - 5
        self.left = fighterLeft - 5
        
if __name__ == '__main__':
    
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
# init the test:
    dramaBackground = pygame.image.load("dramaBackground.png") 
    
    fighterFile = "fighter.png"
    fighterFleet = []
    for i in range(0,9):
        fighter = Fighter(fighterFile, len(fighterFleet))
        fighterFleet.append(fighter)    
    
   #d = DeadFighter("deadFighter10PxA-", 450, 100)
    
    needDeadFighter = True
    while True:
        enviro.screen.blit(dramaBackground, [400,0,330,449])          
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                                   
                if event.key == pygame.K_SPACE:
                    print "do it"
                    if d.paint():
                        print "that's all folks!"
                        
                        
        # A loop like we use to get fighters launched:                
        for i in range (0,9):
            if fighterFleet[i].state == "launching":
                if fighterFleet[i].move() == 0:
                    print "fighter ",i, "READY TO SHOOT!"
                    fighterFleet[i].state = "shoot"
                    
            if fighterFleet[i].state == "shoot" or fighterFleet[i].state == "shooting":
                fighterFleet[i].paint()
            if not (fighterFleet[i].state == "hit" or fighterFleet[i].state == "dead"):
                fighterFleet[i].smokeCheck() 
                
            if fighterFleet[0].state == "shoot" or fighterFleet[0].state == "hit":
                fighterFleet[0].state = "hit"
                if needDeadFighter:
                    needDeadFighter = False
                    d = DeadFighter("deadFighter10PxA-")
                    d.setLocation(fighterFleet[0].rect.left, fighterFleet[0].rect.top)
                else:
                    if d.paint():
                        fighterFleet[0].state = "dead"
                

        myClock.tick(30)
        pygame.display.flip()  
    