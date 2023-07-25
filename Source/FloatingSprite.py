# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import os
from pygame.color import THECOLORS
import enviro # my global game environment


# Floating sprites work properly when speed is a float
# (compare with pygame sprites which don't move properly if not int)
class FloatingSprite(pygame.sprite.Sprite):
    def __init__(self, image_file):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage))
        self.rect = self.image.get_rect()
        
        self.trueLeft = 0
        self.trueTop = 0
        
        self.destX = 0
        self.destY = 0
        
    def calcSpeed(self, steps):

        speedX = (self.destX - self.trueLeft) / steps
        speedY = (self.destY - self.trueTop) / steps
        self.speed = [speedX, speedY]
        
    def __str__(self):
        msg =  "FloatingSprite at x: %.1f y: %.1f" % (self.trueLeft, self.trueTop)
        msg += "  dest x: " + str(self.destX) + " y:" + str(self.destY)
        msg += "  speed x: %.2f y: %.2f" % (self.speed[0], self.speed[1])
        return msg
    
    def paint(self):
        self.rect.left = self.trueLeft
        self.rect.top = self.trueTop
                
        enviro.screen.blit(self.image, self.rect) 
        
    def move(self):
        if self.speed == [0,0]:
            #print "Floating sprite at destination!"
            return 0
        
        #pygame.draw.rect(enviro.screen, THECOLORS["black"], [self.rect.left,self.rect.top,self.rect.width,self.rect.height], 0)
        self.trueLeft = self.trueLeft + self.speed[0]
        self.trueTop = self.trueTop + self.speed[1]

        self.rect.left = self.trueLeft
        self.rect.top = self.trueTop
        #print "Plotting at x=", self.rect.left, "y=",self.rect.top
        #self.rect = self.rect.move(self.speed) # won't work with float!
        
        if self.speed[0] > 0:
            #print "moving right ", self.rect.left, self.speed[0]
            if self.trueLeft + self.speed[0] > self.destX:
                self.speed[0] = self.destX - self.trueLeft
        elif self.speed[0] < 0:
            #print "moving left", self.rect.left, self.speed[0]
            if self.trueLeft + self.speed[0] < self.destX:
                self.speed[0] = self.destX - self.trueLeft
                
        if self.speed[1] > 0:
            #print "moving down ", self.rect.top, self.speed[1]
            if self.trueTop + self.speed[1] > self.destY:              
                self.speed[1] = self.destY - self.trueTop
        elif self.speed[1] < 0:
            #print "moving up ", self.rect.top, self.speed[1]            
            if self.trueTop + self.speed[1] < self.destY:               
                self.speed[1] = self.destY - self.trueTop
            
        #print "float X:", self.rect.left, "Y:",self.rect.top, "destX:",self.destX, "destY:", self.destY, "speedX", self.speed[0], "speedY", self.speed[1]
        enviro.screen.blit(self.image, self.rect)
        if self.rect.left == self.destX:
            self.trueLeft = self.destX
            self.speed = [0,self.speed[1]]
        if self.rect.top == self.destY:
            self.trueTop = self.destY
            self.speed = [self.speed[0], 0]
        return 1
            
    def erase(self):
        pygame.draw.rect(enviro.screen, THECOLORS["black"], [self.rect.left,self.rect.top,self.rect.width,self.rect.height], 0)
        
        
        
        