# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
## Was Color Tower Defense - Menu_Mad_Cloud_Games.py

import pygame
import sys
import os
from pygame.locals import *

import enviro

def run(imageFile, requireKeyToContinue):

    width = 800
    height = 600
    res = (width, height)
    #screen = pygame.display.set_mode(res)
    cover = pygame.Surface(enviro.screen.get_size())
    cover.fill((0,0,0))
    cover_alpha = 255
    alpha_speed = 4
    clock = pygame.time.Clock()
    fps = 30
    TIMER = (3 * fps) # runs for three seconds 
    timer = TIMER


    class Title(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join(enviro.artPathHack,imageFile)).convert()
            self.rect = self.image.get_rect()
            self.rect.center = (width/2, height/2)

    logo = Title()
    infoSprites = pygame.sprite.Group(logo)
    running = True
    quitEarly = False
    readyToExit = not requireKeyToContinue
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                quitEarly = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                quitEarly = True
            elif event.type == pygame.QUIT:
                sys.exit()                
                
        if quitEarly:
            enviro.screen.fill((0,0,0))
            running = False
                
        if running:
            clock.tick(fps)

            timer -= 1
            if timer >= 0:
                cover_alpha -= alpha_speed # make the cover more transparent
                
            elif timer <= 0 and readyToExit: # more covered
                cover_alpha += alpha_speed
                if cover_alpha >= 255:
                    timer = TIMER
                    running = False

            enviro.screen.fill((0,0,0))
            infoSprites.update()
            infoSprites.draw(enviro.screen)
            
            cover.set_alpha(cover_alpha)
            enviro.screen.blit(cover,(0,0))

        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    run()
    pygame.quit()
