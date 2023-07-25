# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
#not sure all of these are needed...
import pygame
import random
import os
from pygame.color import THECOLORS

import enviro # my global game environment
import Noise
    
from AttackerStuff import ShieldSprite
from Harvester import Harvester


class GasFactory(pygame.sprite.Sprite):
    def __init__(self, image_file, left, top, 
                 needStuff0_img, needMoney0_img, needMoney1_img, needMoney2_img, needStuff_img, built_img):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.location = 8
        
        self.need0_white = pygame.image.load(os.path.join(enviro.artPathHack,needStuff0_img))
        self.need0 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney0_img))
        self.need1 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney1_img))
        self.need2 = pygame.image.load(os.path.join(enviro.artPathHack,needMoney2_img))
        self.needStuffToBuild = pygame.image.load(os.path.join(enviro.artPathHack,needStuff_img))
        self.gasFactoryBuilt = pygame.image.load(os.path.join(enviro.artPathHack,built_img)).convert_alpha()
        self.needCount = 0
        self.needXOffset = 20
        self.needYOffset = 60
        self.needType = "none"         
        self.built = 0
        self.padPainted = False
##        if self.built == 1:
##            self.build()

    def paintPad(self):
        enviro.screen.blit(self.image, self.rect)
        self.padPainted = True
        
    def build(self):
        self.built = 1
        enviro.gasFactoryIsBuilt = True
        enviro.screen.blit(self.gasFactoryBuilt, self.rect)
        
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
            