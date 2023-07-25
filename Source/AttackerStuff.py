# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import random
import os
from pygame.color import THECOLORS

import enviro # my global game environment
from FloatingSprite import FloatingSprite
from Fighter import Fighter


    
# Need a sprite to represent the shield, so we can test collision
class ShieldSprite(pygame.sprite.Sprite):

    def __init__(self, image_file, left, top, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,image_file)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left = left
        self.rect.top = top
        self.rect.width = width
        self.rect.height = height
        
    # just for testing, this thing isn't drawn ever
    def paint(self):
        enviro.screen.blit(self.image, self.rect)