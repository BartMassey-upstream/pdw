# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import random
import sys # for testing
from pygame.color import THECOLORS

import enviro # my global game environment
from FloatingSprite import FloatingSprite

class Fighter(FloatingSprite):
    def __init__(self, image_file, fleetCount):
        
        FloatingSprite.__init__(self, image_file)
        self.maxBombs = 1
        self.bewareILive(fleetCount)
        self.bombsOut = 0
        
##        smoke_surface = pygame.surface.Surface([10,10])
##        smokeArray = pygame.surfarray.pixels2d(smoke_surface)
##        smokeArray[0][0] = 255
##        smokeArray[9][9] = 255
##        smokeOut = pygame.surfarray.make_surface(smokeArray)
##        smokeOut.convert()
##        
##        enviro.screen.blit(smokeOut, [10,10])
        
    def __str__(self):
        msg = FloatingSprite.__str__(self)
        msg +=  "  Fighter state:" + str(self.state)
        return msg         
        
    def bewareILive(self, fleetCount):
        self.trueLeft = 552 # 552 will start right below mother
        self.trueTop = 21 # 21 will start right below mother
        
        if fleetCount > -1:
            self.fleetPosition = fleetCount        
        
##        fighterSpots = [ [560,91], [440,91], [500,91], [620,91], [680,91],
##                            [470,71], [650,71], [590,71], [530,71]]
        fighterSpots = ( (500,91), (680,91), (440,91), (620,91), (560,91),
                            (470,71), (650,71), (590,71), (530,71) )                            
        self.destX = fighterSpots[self.fleetPosition ][0]
        self.destY = fighterSpots[self.fleetPosition ][1]
        
        self.calcSpeed(enviro.FIGHTER_LAUNCH_SPEED) # maybe 30.0 good for prod?
        
        self.state = "launching"
        self.fullHealth = 150
        self.life = self.fullHealth
        
    def smokeCheck(self):
        top = self.rect.top+9
        left = self.rect.left
        if self.life > 0:
            lifebar = (float(self.life)/self.fullHealth) * 20
            pygame.draw.lines(enviro.screen, [255,255,255], False, [ [left,top],[left+lifebar,top]], 1)
        
    def test(self, targetSprite, nextState, laserPower):
        # see if this fighter is it by the targeting sprite, if so set the next state

        hitMe = False
        killedMe = False
        tester = pygame.sprite.Group()
        tester.add(targetSprite)
        if pygame.sprite.spritecollideany(self, tester):
            #print "FIGHTER HIT! Laser power=", enviro.LASER_POWER
            hitMe = True
            self.life = self.life - laserPower
            if self.life < 1:
               self.state = nextState
               killedMe = True
        return [hitMe, killedMe]
    
    def takeAShot(self):
        randShot = random.randint(1,10)
        if randShot == 1:
            if self.bombsOut < self.maxBombs:
               self.state = "shooting"
               self.bombsOut = self.bombsOut + 1
               return True
        return False
    
    def shotExpired(self):
        self.bombsOut = self.bombsOut - 1
        if self.state <> "hit" and self.state <> "launching":
            self.state = "shoot"
            
        
if __name__ == '__main__':
    
    print "TEST: fighter"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
# stuff needed for init: 
    dramaBackground = pygame.image.load("dramaBackground.png")   
    fighterFile = "fighter.png"

    fighterFleet = []

    for i in range(0,9):
        fighter = Fighter(fighterFile, len(fighterFleet))
        fighterFleet.append(fighter)
       

#    fightersActive = 1
            
    while True:


    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (event.type == pygame.KEYDOWN):
            if (pygame.key.get_mods() == 1024): # command key
                if (event.key == 113):   # q
                    sys.exit()
            if event.key == pygame.K_x:                    
                fighterFleet[0].life = fighterFleet[0].life - 1
                    
            if event.key == pygame.K_SPACE:                    
                fighterFleet[0].smokeCheck()
                    
        enviro.screen.blit(dramaBackground, [400,0,330,449])                    

        for i in range (0,9):
            if fighterFleet[i].state == "launching":
                if fighterFleet[i].move() == 0:
                    print "fighter ",i, "READY TO SHOOT!"
                    fighterFleet[i].state = "shoot"
                    
            if fighterFleet[i].state == "shoot" or fighterFleet[i].state == "shooting":
                fighterFleet[i].paint()
            if i == 0:
                fighterFleet[i].smokeCheck()
        
        myClock.tick(30)
        pygame.display.flip()                 