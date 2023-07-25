# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame, random
from pygame.color import THECOLORS
import sys    # for testing
import os
from pygame.locals import *

import enviro # my global game environment
import Noise
from FloatingSprite import FloatingSprite
from AttackerStuff import *
from DeadFighter import DeadFighter
# Third-party source, now piled in with the rest, package refactoring no fun
import gradients

import Bomb

class MotherShip(pygame.sprite.Sprite):
    def __init__(self, image_file, fighterFleet, bomb_image):
        
        pygame.sprite.Sprite.__init__(self)
        self.theImage = image_file
        self.image = pygame.image.load(os.path.join(enviro.artPathHack,self.theImage))
        self.rect = self.image.get_rect()
        
        self.fighterFleet = fighterFleet
        self.buildCount = 0
        self.activeFighters = 0
        
        self.state = "Waiting"
        self.waitCount = enviro.MOTHER_START_WAIT #200 good for prod?
        self.rect.left = enviro.MOTHER_START_POSITION #810 good for prod, off the screen
        self.rect.top = 0
        self.diedAt = 0 # when she dies we'll stash the spot here...
        
        self.bomb_img_file = bomb_image
        
        self.fullHealth = 300
        self.life = self.fullHealth
        
        self.fasterNextTime = 300
        
        self.deadFighterList = []
        self.enterNoiseCounter = 0
        self.hitCount = 0
        
    def test(self, targetSprite, nextState, laserPower):
        # given a bomb and the shield object, see if we hit the shield

        hitMe = False
        killedMe = False
        tester = pygame.sprite.Group()
        tester.add(targetSprite)
        if pygame.sprite.spritecollideany(self, tester):
            #print "MOTHER HIT!"
            hitMe = True
            self.life = self.life - laserPower
            if self.life < -1:
               self.state = nextState
               killedMe = True
        return [hitMe, killedMe]        
        
    def getFleetSize(self):
        return len(self.fighterFleet)
    
    def getFighterFleet(self):
        """ Get a list of active fighters"""
        
        myFleet = []
        for i in range (0,self.activeFighters):
            if not self.fighterFleet[i].state == "hit":
                myFleet.append(self.fighterFleet[i])
            
        return myFleet
    
    def notifyDeadFighter(self,fighter):
        fighterDeathFileName = "deadFighter10PxA-"
        anotherDead = DeadFighter(fighterDeathFileName)        
        
        #anotherDead = enviro.deadFighterModel
        anotherDead.setLocation(fighter.rect.left, fighter.rect.top)
        """ One of the active fighters is dead! """
        self.deadFighterList.append(anotherDead)
        
    def paint(self, bombList, fighterCount):
        
        self.life = self.life + 1
        if self.life > self.fullHealth:
            self.life = self.fullHealth
        
        dramaState = 0 # 0=nothing, 1=shield is hit
        
##        for deadFighter in self.deadFighterList:
##            print deadFighter
##            if deadFighter.paint():
##                print "done"            
##        print
        for i in range (len(self.deadFighterList)-1, -1, -1):
            #print i
            #print self.deadFighterList[i]
            if self.deadFighterList[i].paint():
                #pass
                del self.deadFighterList[i]
        #print "Dead list len=", len(self.deadFighterList)

        #if self.state == "Fighting" or self.state == "Hit":
        if True:
            #print "Bombs=", len(bombList)
            for bomb in bombList:
                if bomb.state == "caught":
                    #print "caught bomb launched from ", bomb.fromFighter
                    self.fighterFleet[bomb.fromFighter].shotExpired()

                    dramaState = 1
                    bombList.remove(bomb)
                elif bomb.state == "hit":
                    bomb.paint()
                    bomb.explode()
                elif bomb.state == "dead":
                    #print "Dead bomb from fighter", bomb.fromFighter
                    #self.fighterFleet[bomb.fromFighter].state = "shoot"
                    self.fighterFleet[bomb.fromFighter].shotExpired()
                    bombList.remove(bomb)
                    
            for i in range (0,self.activeFighters):
                #print self.fighterFleet[i]
                if self.fighterFleet[i].state == "launching":
                    if self.fighterFleet[i].move() == 0:
                        self.fighterFleet[i].state = "shoot"
                if (self.fighterFleet[i].state == "shoot" or 
                   self.fighterFleet[i].state == "shooting"):
                    if self.fighterFleet[i].takeAShot():
                        randX = random.randint(1,80) - 40
                        myBomb = Bomb.Bomb(self.bomb_img_file,
                                    self.fighterFleet[i].trueLeft+6,
                                    self.fighterFleet[i].trueTop+8,
                                    self.fighterFleet[i].trueLeft+6 + randX-5,
                                    430, i) # stupid bomb object won't load
                        bombList.add(myBomb)
                if (self.fighterFleet[i].state == "shoot" or 
                   self.fighterFleet[i].state == "shooting"):
                    self.fighterFleet[i].paint()
                if self.fighterFleet[i].state <> "hit":
                    self.fighterFleet[i].smokeCheck()
                    
        if self.state == "Fighting":
            if self.buildCount > 0 and enviro.test == 1:
                pygame.draw.lines(enviro.screen, [255,255,255], False, [[400,0],[400+self.buildCount,0]], 1)
            fighterNeedsRebuild = False                    
            for i in range(0, self.activeFighters):
                if self.fighterFleet[i].state == "hit":
                    fighterNeedsRebuild = True
                    break
            if fighterNeedsRebuild or self.activeFighters < fighterCount:
                self.buildCount = self.buildCount + 1
                if self.buildCount > enviro.MOTHER_BUILD_SPEED:
                    self.buildCount = 0
                    builtFighter = False
                    for i in range(0, self.activeFighters):
                        if self.fighterFleet[i].state == "hit":
                            self.fighterFleet[i].bewareILive(-1)
                            #print "revived fighter!"
                            self.fighterFleet[i].paint()
                            builtFighter = True
                            break
                    if not builtFighter:
                        self.activeFighters = self.activeFighters + 1
                        #print "now there are ",self.activeFighters, "fighters"
                        self.fighterFleet[self.activeFighters-1].paint()
                        
        if self.state == "Waiting":
            self.waitCount = self.waitCount - 1
            if self.waitCount < 1:
                self.state = "Approaching"
                
        if self.state == "Approaching":
            #print "centertest", self.rect.center
            if self.rect.left > 530:
                pygame.draw.rect(enviro.screen, THECOLORS["black"], [self.rect.left,self.rect.top,60,20], 0)
                self.rect.left = self.rect.left - 3
                if self.rect.left % 10 == 0 and self.rect.left > 580:
                    channel = pygame.mixer.find_channel(True)
                    if channel:
                        #print "got channel"
                        channel.play(enviro.soundEffect[Noise.MOTHER_ENTERS])
                    else:
                        print "no channel for mother kill sound, will try to use main"
                        enviro.soundEffect[Noise.MOTHER_HIT].play()                
            else:
                self.state = "Ready"
                
        if self.state == "Ready":
            if self.activeFighters == 0:
                self.activeFighters = 1
            #self.fighterFleet[0].paint() # paint the new fighter
            self.state = "Fighting"
       
        if self.state <> "Hit" and self.state <> "Waiting":    
           enviro.screen.blit(self.image, self.rect)
           self.paintHealthMeter()
        else:
            pygame.draw.rect(enviro.screen, [0,0,0], [740,126,30,300], 0) 
            
        if self.state == "Hit":
            self.hitCount += 1
            #print "The mother has died ",self.hitCount," times, do we need a mercy rule?"
            self.state = "Waiting"
            self.waitCount = enviro.MOTHER_RESTART_WAIT - self.fasterNextTime
            if self.waitCount < 0:
                self.waitCount = enviro.MOTHER_MIN_RESTART
            self.fasterNextTime = self.fasterNextTime + 100
            self.buildCount = 0
            self.diedAt = self.rect.left
            self.rect.left = enviro.MOTHER_START_POSITION
            self.fullHealth = self.fullHealth + enviro.MOTHER_LIFEGAIN_PER_LEVEL
            enviro.MOTHER_BUILD_SPEED = enviro.MOTHER_BUILD_SPEED - 150
            if enviro.MOTHER_BUILD_SPEED < 200:
                enviro.MOTHER_BUILD_SPEED = 200
            
            self.life = self.fullHealth
            
        return [bombList, dramaState, self.state]
        
                         
    def paintHealthMeter(self):
        pygame.draw.rect(enviro.screen, [128,128,128], [740,126,30,300], 0)
        if self.life > 0:
            
            #paintLifeBar = self.life
            paintLifeBar = (float(self.life) / self.fullHealth) * 296
            #paintLifeTop = 296-self.life
            paintLifeTop = 296 - paintLifeBar
            
            #pygame.draw.rect(enviro.screen, [255,255,255], [742,128+paintLifeTop,26,paintLifeBar], 0)
            enviro.screen.blit(gradients.vertical_func((26,int(paintLifeBar)),(255,255,255),(255,0,0)), (742,128+paintLifeTop))

        
if __name__ == '__main__':
    
    print "TEST: mothership"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
# stuff needed for init: 
    enviro.soundEffect = []
    enviro.soundEffect.append(Noise.load_sound('63068__radian__odd_trimmedAndReworked.wav'))
    Noise.MOTHER_ENTERS = len(enviro.soundEffect) - 1 

    dramaBackground = \
       pygame.image.load(os.path.join(enviro.artPathHack,'dramaBackground.png'))
    fighterFile = "fighter.png"

    fighterFleet = []

    for i in range(0,9):
        fighter = Fighter(fighterFile, len(fighterFleet))
        fighterFleet.append(fighter)

    motherShipFile = "mother.png"
    bomb_image = "bomb.png"
    
    enviro.MOTHER_START_WAIT = 10

    m = MotherShip(motherShipFile, fighterFleet, bomb_image)
    
    bombList = pygame.sprite.Group()
    fightersActive = 1
    
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (event.type == pygame.KEYDOWN):
            if (pygame.key.get_mods() == 1024): # command key
                if (event.key == 113):   # q
                    sys.exit()
            if event.key == pygame.K_SPACE:                    
                m.life = m.life - 10
                    
        enviro.screen.blit(dramaBackground, [400,0,330,449])                    
                    
        theMother = m.paint(bombList, fightersActive) # paint her progress, and get any emitted bombs  
        
        myClock.tick(30)
        pygame.display.flip()                           
        