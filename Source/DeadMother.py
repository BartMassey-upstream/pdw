# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import sys # for testing
import os
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise
from Fighter import Fighter # for testing...
from MotherShip import MotherShip # for testing...

class DeadMother:
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
        msg =  "  Dead mother X:" + str(self.top) + " Y:" + str(self.left)
        msg += "    frameCount=" + str(self.deathFrameCount)
        return msg               
            
    def paint(self):
        deathFrame = self.deathFrameCount 
        #print "  deathframe=", deathFrame
        # maybe we got called too many times... if so, let's not crash
        if deathFrame >= len(self.deathImage):
            return False
        enviro.screen.blit(self.deathImage[deathFrame], [self.left, self.top])
        self.deathFrameCount += 1
        nextFrame = self.deathFrameCount 
        # the intention is to signal when we're done, and shouldn't be called again...
        if nextFrame >= len(self.deathImage):
            return False
        return True
    
    def setLocation(self,fighterLeft, fighterTop):
        self.top = fighterTop
        self.left = fighterLeft - 20
        self.deathFrameCount = 0
        
if __name__ == '__main__':
    
    print "TEST: dead mothership"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
# stuff needed for init: 
    enviro.soundEffect = []
    enviro.soundEffect.append(Noise.load_sound('63068__radian__odd_trimmedAndReworked.wav'))
    Noise.MOTHER_ENTERS = len(enviro.soundEffect) - 1 
    
    dramaBackground = pygame.image.load("dramaBackground.png")   
    fighterFile = "fighter.png"

    fighterFleet = []

    for i in range(0,9):
        fighter = Fighter(fighterFile, len(fighterFleet))
        fighterFleet.append(fighter)

    motherShipFile = "mother.png"
    bomb_image = "bomb.png"
    
    enviro.MOTHER_START_WAIT = 10
    enviro.MOTHER_RESTART_WAIT = 10  
    enviro.MOTHER_MIN_RESTART = 10    

    m = MotherShip(motherShipFile, fighterFleet, bomb_image)
    
    bombList = pygame.sprite.Group()
    fightersActive = 1
    
    needDeadMother = False
    sheDied = False
    dead = DeadMother("motherDead-") 
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN):
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                        
                if event.key == pygame.K_SPACE:                    
                    m.state = "Hit"
                    needDeadMother = True

                    
        enviro.screen.blit(dramaBackground, [400,0,330,449])                    
                    
        theMother = m.paint(bombList, fightersActive) # paint her progress, and get any emitted bombs
        print m.rect.left
        if needDeadMother:

            dead.setLocation(m.diedAt,0) 
            needDeadMother = False
            sheDied = True
            
        if sheDied:
            dead.paint()
        
        myClock.tick(30)
        pygame.display.flip()      
 
    