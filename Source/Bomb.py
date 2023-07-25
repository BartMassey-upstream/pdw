# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import random
import os

from pygame.color import THECOLORS
import sys # for testing

import enviro # my global game environment
from FloatingSprite import FloatingSprite
from Fighter import Fighter

     
class Bomb(FloatingSprite):
    def __init__(self, image_file, x, y, destX, destY, fromFighter):
        self.image = image_file
        FloatingSprite.__init__(self, self.image)
        
        self.fromFighter = fromFighter
        self.state = "blam"
        self.death = 0
        
        self.trueLeft = x
        self.trueTop = y
        
        self.destX = destX
        self.destY = destY
        self.calcSpeed(200.0) # 200 steps is good, define this as float!
        
        self.detonate = 0
        self.detonation = 0
        self.nuked = False
        
    def test(self, shieldSprite, nextState):
        # given a bomb and the shield object, see if we hit the shield
        
        if self.rect.top == 430:
            return False 

        tester = pygame.sprite.Group()
        tester.add(shieldSprite)
        if pygame.sprite.spritecollideany(self, tester):
            #print "CAUGHT!"
            self.state = nextState
            return True
        return False
 
# this is provided by floating sprite, duh!   
##    def paint(self):
##        enviro.screen.blit(self.image, self.rect)
    
    def nuke(self):
        self.detonate = self.detonate + 2
        if self.detonate % 5 == 0:
            self.detonation = self.detonation + 5
        for i in range (10,self.detonate,10):
             self.circleIt(i)         
        if self.detonate > 150:
            self.nuked = True
    
    def circleIt(self, radius):
        #pygame.draw.circle(enviro.screen, [255,255,255], [self.rect.left,self.rect.top], 20, 3)
        
        #drawcircle(image, colour, origin, radius, width=0)
        enviro.drawcircle(enviro.screen, [255,255,255], [self.rect.left+4,self.rect.top+5], radius, 3)
            
    def explode(self):
        self.speed = [0,0]
        #print "death=",self.death
        
        if self.death == 0:
            self.oldCenter = self.rect.center

        self.death = self.death + 5
        
        
        if self.death > 30:
            self.theImage = "deadBomb4.png"
        elif self.death > 20:
            self.theImage = "deadBomb3.png"
        elif self.death > 10:
            self.theImage = "deadBomb2.png"
        else:
            self.theImage = "deadBomb1.png"
            
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.oldCenter
                
        if self.death > 40:
           self.state = "dead"
            
    def __str__(self):
        msg = FloatingSprite.__str__(self)
        msg +=  "  Bomb state:" + str(self.state)
        return msg  
    
if __name__ == '__main__':
    
   
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
# stuff needed for init:

    artPath = os.path.join('..','art')
    dramaBackground = \
        pygame.image.load(os.path.join(artPath,'dramaBackground.png'))

 
    b = Bomb("bomb.png",600,200,600,430, 0)
    
    while True:
        enviro.screen.blit(dramaBackground, [400,0,330,449])          
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
               
                if event.key == pygame.K_h:
                    print "hit"

        b.paint()
        if not b.nuked:
           b.nuke()
   
        
        myClock.tick(30)
        pygame.display.flip()    