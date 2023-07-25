# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
# Gotta love noise!
# I used music and sound code from http://www.pygame.org/project-Arcade+Tonk+Tanks-1078-2412.html

# missioneers2? 4 is better


import pygame
import os.path

import enviro # my global game environment

SHIELD_HIT = 0
BOMB_HIT = 0
LASER_MISS = 0

class dummysound:
    # good idea but seems hopeless... so it must not fail!
    def play(self): pass
    def set_volume(self, volume): pass

def load_sound(file):
    #print 'Loading sounds...can I get the mixer?'
    if not pygame.mixer: return dummysound()
    #file = os.path.join('..','Sound', file)
    file = os.path.join(enviro.soundPathHack, file)
    try:
        testFile = open(file, "r")
        sound = pygame.mixer.Sound(file)
        #print 'Sound loaded'
        return sound
    except pygame.error:
        print 'Warning, unable to load sound', file
    except IOError:
        print 'Warning, IO error loading sound', file
    return dummysound()

def initMixer():
    if pygame.mixer and not pygame.mixer.get_init():
        print 'WARNING: sound init failed!'
        pygame.mixer = None

def playMusic(file):
    if pygame.mixer:
        music = os.path.join('Sound', file)
        
        pygame.mixer.music.load(music)
        # The old way, was pretty good but now it's a lot better
        #pygame.mixer.music.set_volume(enviro.musicLevel[1])
        #pygame.mixer.music.set_volume(enviro.musicLevel[enviro.musicVolume])
        #pygame.mixer.music.set_volume(enviro.musicVolumeController.setting/100.0) 
        pygame.mixer.music.play(-1)
    
class Volume(pygame.sprite.Sprite):
    def __init__(self, theScreen, location=[0,0], size=[100,20], init=50):
        
        self.screenSurface = theScreen
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface([10,int(size[1]*.8)])
        image_surface.fill([255,255,255])
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.controlLocation = location
        self.controlSize = size
        
        self.setting = init
        
        self.mousePosition = [0,0]
        
    def paintControl(self):
        left = self.controlLocation[0]
        top = self.controlLocation[1]
        width = self.controlSize[0]
        height = self.controlSize[1]
        
        pygame.draw.rect(self.screenSurface, [100,100,100], [left-5,top,width+10,height])
        
        lineInMiddle = top+height/2
        pygame.draw.lines(self.screenSurface, [200,200,200], False, [[left,lineInMiddle],[left+width,lineInMiddle]], 1)
        for i in range(0,6):
            if i == 0 or i == 5:
                markTop = top+2
                markBot = top + height -4
            else:
                markTop = lineInMiddle - self.controlSize[1]*.2
                markBot = lineInMiddle + self.controlSize[1]*.2
            pygame.draw.lines(self.screenSurface, [200,200,200], False, [[left+i*(width/5),markTop],[left+i*(width/5),markBot]], 1)
        offset = (self.setting/100.0)*width
        self.rect.centery = lineInMiddle 
        self.rect.centerx = left+offset
        self.screenSurface.blit(self.image, self.rect)
        
    def mouseOnControl(self,mousePos):
        left = self.rect.left
        top = self.rect.top
        width = 10
        height = self.controlSize[1]*.8
        
        if (mousePos[0] > left and 
           mousePos[0] < left+width and 
           mousePos[1] > top and 
           mousePos[1] < top+height):
            self.mousePosition = mousePos
            return True
        return False
    
    def setLevel(self,mousePos):
        self.setting += (mousePos[0] - self.mousePosition[0])/2
        if self.setting < 0:
            self.setting = 0
        if self.setting > 100:
            self.setting = 100
        self.mousePosition = mousePos
        
    def setLevelByClick(self, mousePos):
        left = self.controlLocation[0]
        top = self.controlLocation[1]
        width = self.controlSize[0]
        height = self.controlSize[1]
                
        if (mousePos[0] > left and 
           mousePos[0] < left+width and 
           mousePos[1] > top and 
           mousePos[1] < top+height):
             
            if mousePos[0] < self.rect.centerx:
                self.setting -= 20
            else:
                self.setting += 20
            self.setting = int(round(self.setting / 20.0) * 20)
                
            
            if self.setting < 0:
                self.setting = 0
            if self.setting > 100:
                self.setting = 100
            return True
        return False
        
    
        
if __name__ == '__main__':
    
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
    v = Volume(enviro.screen,location=[300,250], size=[250,40], init=100)
    v.paintControl()
    
# stuff needed for init:
            
    heldDown = False
    
    playMusic('Allmyownworkv2.mp3')
    pygame.mixer.music.set_volume(1) 
    
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mousePos = event.pos
                if heldDown:
                    v.setLevel(mousePos)
                    print v.setting
                    pygame.mixer.music.set_volume(v.setting/100.0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                heldDown = v.mouseOnControl(mousePos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if heldDown == False:
                    v.setLevelByClick(mousePos)
                    print v.setting
                    pygame.mixer.music.set_volume(v.setting/100.0)
                heldDown = False

            elif (event.type == pygame.KEYDOWN):
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                        
                if event.key == pygame.K_SPACE:
                    print "Generate!"
                   
        v.paintControl()        
        
        myClock.tick(30)
        pygame.display.flip()               