#! /usr/bin/env python
# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
#
# ProduceDefendWin.py
#  My first Pygame, an execuse to learn Python and teach my man Steven
#
# Version history:
#   1.1 - Tidy up, fix some graphics, smarter bots, fixed mothership "mercy"
#         bug where she'd stop coming after about 8 kills... I forget what
#         else, version history what a concept! 
#
#   1.0 - Project completed, I'm actually releasing a "finished" game!
#
# Rambling:
# 1.1 I've watched a bit of beta play and really need to do something about
# the standoff condition when the player misses "ideal strategy" and ends up
# just killing the mothership over and over. If we were in the arcades the
# choice would be easy -- just slaughter the player and demand another
# quarter. Maybe that's best but seems mean... though the alternative is to
# let them win and that's no good either. For now I'll just release and keep
# thinking about this.
#
# 1.0 My first Python game, learned a lot and there's a ton I'd do 
# differently but rather than spend more time here... get it out and move on. 
# I'm interested in any comments anyone would have. Reasonably satisified
# with how it turned out :)
# --------------------------------------------------------------------------
#
# I've left a ton of crummy notes to myself in the code, here are a few:
#
# I used Stanti's Python Editor for this, good stuff.
# First thing, I added a shortcut to
# /applications/SPE.app/Contents/Resources/_spe/shortcuts/Macintosh.py
# Now it ends with:
#   'Run in terminal without arguments  exit'    : 'Ctrl+Shift+X',
# Fast interative development, SWEET!
#
#
#pygame.mouse.set_visible(0)  # interesting? hides mouse in window


import pygame
import sys
import random
import re # for pyconsole
import os.path
from pygame.mixer import *
from pygame.color import THECOLORS
from pygame.locals import *

from Source import pyconsole
from Source import pyconsole_syntax
#    re_add, console_add, re_function, console_func ## took the easy way out
from Source import pyconsole_functions, fps, cheat, line

from Source import enviro # my global game environment
from Source import Noise # all the music and effects stuff should be here

from Source import YourStuff
from Source import AttackerStuff
from Source import Fighter
from Source import FloatingSprite
from Source import Harvester
from Source import MotherShip
from Source import GasFactory
from Source import Laser
from Source import Shields
from Source import Bomb
from Source import DeadMother
from Source import Generator

from Source import Title
from Source import mainline


def main(continuing, firstRun):
    
    if firstRun:
        if enviro.testEntryScreenSkip <> 1:
            Title.run("myTitle.png", False)
            Noise.playMusic('JMICKEL_Allmyownworkv2.mp3')
            pygame.mixer.music.set_volume(enviro.INIT_MUSIC/100.0)            
            Title.run("instructions.png", True)
        else:
            Noise.playMusic('JMICKEL_Allmyownworkv2.mp3')
            pygame.mixer.music.set_volume(enviro.INIT_MUSIC/100.0)             
    else:
        Noise.playMusic('JMICKEL_Allmyownworkv2.mp3')          
    
    if not continuing:
        enviro.credits = 0
        enviro.shields.upgrades = 1
        enviro.laser.upgrades = 1
        enviro.gasFactoryIsBuilt = False
        enviro.botFactoryIsBuilt = False
        enviro.BOMB_POWER = 500
        
        # Difficulty menu
        if enviro.testMenuSkip <> 1:
            difficulty = mainline.menu()
        else:
            difficulty = "Normal"
        enviro.difficultyForContinue = difficulty        
    else:
        difficulty = enviro.difficultyForContinue
        
    if enviro.test == 1:
        enviro.credits = 20000
        

    # Draw the pads, the base, get me a you, create some gas, all that stuff...
    enviro.start(difficulty)
    #mainline.varInfo(enviro)

    if enviro.gasFactoryIsBuilt:
        enviro.gasFactory.build()
    else:
        enviro.gasFactory.built = 0 # seems we need this for restart
    
    if enviro.botFactoryIsBuilt:
        enviro.factory.build()
    else:
        enviro.factory.built = 0
        
    mainline.writeInstructions(difficulty)
    enviro.writeCredits(enviro.credits)

    shieldPower = enviro.START_SHIELD_POWER
    maxFighters = enviro.fleetMax

    # The first one's free...
    newGen = Generator(5,enviro.gasGauges, "generator0.png")
    newGen.refill(enviro.gasGauges)
    enviro.generators.append(newGen)
    
    
    dramaBackground = \
        pygame.image.load(os.path.join(enviro.artPathHack,'dramaBackground.png'))    
    
    # Yes, I could have made even more of these
    demoStep = 0
    motherBecameActive = False
    fightersActive = 1
    frustration = 0
    shooter = False
    paused = False
    shooting = False
    theKillerBomb = None
    deadMother = DeadMother("motherDead-")
    sheDied = False 
    sheIsDead = False
    musicVolumeControllerMouseHeldDown = False
    effectsVolumeControllerMouseHeldDown = False
    linePainted = False
    needHint = True
    
    console = pyconsole.Console(
        enviro.screen, # my screen
        (401,0,328,449), # the drama area - gets refreshed every cycle, required for console
        functions={"FPS":fps,"cheat":cheat,"credits":credits, "line":line}, # functions for the console
        key_calls={"d":sys.exit}, # ctrl+d calls sys.exit()
        syntax={pyconsole_syntax.re_add:pyconsole_syntax.console_add, pyconsole_syntax.re_function:pyconsole_syntax.console_func}
        )
    
    mousePos = [0,0]
    bombList = pygame.sprite.Group()
    
    # Steven learned about the word "bailout" today so that's on my mind
    # as I wrestle with what to do if somebody gets cute... be cute right back!
    # It's a little buggy but that's what happens with bailouts.
    # Works well enough I shouldn't get thrown out of office, or something.
    bailoutCount = 0

    alive = 1        
    while alive == 1:
        
        releasedButton = False

        console.process_input()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_w and pygame.key.get_mods() & KMOD_CTRL:
                    console.set_active()
                elif event.key == K_1 and pygame.key.get_mods() & KMOD_CTRL: 
                #elif event.key == K_1 and (pygame.key.get_mods() == 64 or pygame.key.get_mods() == 128): 
                    # "Just a little hack so you can play with both pyconsole and python"
                    # Hit ctrl w to hide pyconsole, then ctrl 1 to switch modes, then ctrl w again to show the console
                    console.setvar("python_mode", not console.getvar("python_mode"))
                    console.set_interpreter() 
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if paused:
                        enviro.writePaused(False)
                        paused = False
                    else:
                        enviro.writePaused(True)
                        paused = True
                        enviro.musicVolumeController.paintControl() 
                        enviro.effectsVolumeController.paintControl()
                        enviro.screen.blit(pygame.image.load(os.path.join(enviro.artPathHack,"effectsIcon.png")), [10,570])
                        enviro.screen.blit(pygame.image.load(os.path.join(enviro.artPathHack,"musicIcon.png")), [170,570]) 
                elif (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q  -- so Apple-Q quits like other programs on OS X
                        sys.exit()
                elif event.key == K_q and pygame.key.get_mods() & KMOD_CTRL: # ctrl-q like most games
                    sys.exit()
                    
                if enviro.cheatKeys:
                    if event.key == pygame.K_h and pygame.key.get_mods() & KMOD_CTRL:
                        print "HARVESTER DEBUG"
                        for harvester in enviro.harvesters:
                            print harvester
                    elif event.key == pygame.K_t:
                        enviro.theBase.stashStuff()
                    elif event.key == pygame.K_n:
                        print "NUKE"
                        alive = 0
                    elif event.key == pygame.K_u:
                        print "WIN"
                        alive = 0
                        enviro.credits = 1000000
                    elif event.key in enviro.genKeys:
                        mainline.cheatKeys(event.key)                               
                    
                if paused:
                    #print pygame.key.name(109) # the name of a key code
                    break # no actions will be processed until unpause
                
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:        
                    enviro.you.aimLeft(enviro.pads)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    enviro.you.aimRight(enviro.pads)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    enviro.you.aimUp(enviro.pads)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    enviro.you.aimDown(enviro.pads)
                if event.key == pygame.K_SPACE:
                    action = enviro.you.interact(enviro.generators, 
                                                 enviro.shields, 
                                                 enviro.theBase, 
                                                 enviro.laser)
                    if action[0] > -1 and action[1] == 1:
                        # build a generator
                        enviro.doAction(enviro.you, 
                                        action, 
                                        enviro.gasGauges)                       
                        
            elif event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # There's too much code here... next time!
                mousePos = event.pos
                if musicVolumeControllerMouseHeldDown:
                    enviro.musicVolumeController.setLevel(mousePos)
                    pygame.mixer.music.set_volume(enviro.musicVolumeController.setting/100.0)  
                if effectsVolumeControllerMouseHeldDown:
                    enviro.effectsVolumeController.setLevel(mousePos)
                    for effect in enviro.soundEffect:
                        effect.set_volume(enviro.effectsVolumeController.setting/100.0)                                

                newCursor = event.pos
                if (enviro.combatStarted and 
                   (newCursor[0] > 400 and 
                    newCursor[0] < 730 and 
                    newCursor[1]<430)):
                    pygame.mouse.set_cursor(*enviro.LASER_POINTER)
                    shooter = True
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)
                    shooter = False
                    shooting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                musicVolumeControllerMouseHeldDown = \
                  enviro.musicVolumeController.mouseOnControl(mousePos)
                effectsVolumeControllerMouseHeldDown = \
                  enviro.effectsVolumeController.mouseOnControl(mousePos)
                
                if shooter and not paused:
                    shooting = True

            elif event.type == pygame.MOUSEBUTTONUP:
                
                if musicVolumeControllerMouseHeldDown == False:
                    enviro.musicVolumeController.setLevelByClick(mousePos)
                    pygame.mixer.music.set_volume(enviro.musicVolumeController.setting/100.0)
                musicVolumeControllerMouseHeldDown = False
                if effectsVolumeControllerMouseHeldDown == False:
                    if enviro.effectsVolumeController.setLevelByClick(mousePos):
                        for effect in enviro.soundEffect:
                            effect.set_volume(enviro.effectsVolumeController.setting/100.0)
                effectsVolumeControllerMouseHeldDown = False                                 
                
                releasedButton = True
                
            #print pygame.key.get_mods()  # show modifier keys
            #if (event.type == KEYUP) or (event.type == KEYDOWN): # show key
            #    print "DEBUG KEY:", event
                            
        """ now do all the stuff that happens each frame: """
 
        enviro.musicVolumeController.paintControl() 
        enviro.effectsVolumeController.paintControl()
        
        if paused and enviro.combatStarted == False and demoStep == 10: 
            demoStep += 1

        if not paused:
            if enviro.combatStarted == False and demoStep > 10:
                mainline.startCombat()
                
            enviro.paintRoadTiles()
                    
            if enviro.combatStarted:
                enviro.screen.blit(dramaBackground, [400,0,330,449])
            else:
                [demoStep, bailoutCount, alive] = mainline.demoMode(demoStep, bailoutCount, alive)
                #print bailoutCount
                    
            for generator in enviro.generators:
                generator.produce(enviro.gasGauges)
            if enviro.combatStarted:
                shieldPower = enviro.shields.powerUp(shieldPower, enviro.fuelPile)
                shieldSprite = enviro.shields.paintShield(shieldPower)

                frustration += 1
                if frustration > enviro.MOTHER_FLEET_INCREASE_WAITTIME:
                    frustration = 0
                    fightersActive += 1
                    if fightersActive > maxFighters:
                       fightersActive = maxFighters            

                # paint her progress, and get any emitted bombs
                theMother = enviro.mother.paint(bombList, fightersActive) 
                bombList = theMother[0]
                drama = theMother[1]
                herState = theMother[2]
                
                if sheIsDead:
                    deadMother.setLocation(enviro.mother.diedAt,0)
                    sheDied = True
                    sheIsDead = False
                
                if not herState == "Waiting":
                    if not motherBecameActive:
                        motherBecameActive = True
                        if pygame.mixer:
                            Noise.playMusic('JMICKEL_ViperFantastic.mp3')
                            
                if drama == 1:
                    shieldPower = shieldPower - enviro.BOMB_POWER
                    if shieldPower < 0:
                        shieldPower = 0
                    enviro.shields.hitShield(shieldPower)
                    enviro.shields.paintShield(shieldPower)
                    enviro.soundEffect[Noise.SHIELD_HIT].play()
                    if needHint and (difficulty == "Easy" or difficulty == "Normal"):
                        linePainted = mainline.writeHelpfulHintLine(linePainted)
                    
                if len(bombList) > 0:
                    for bomb in bombList:
                        if bomb.move() == 0 and bomb.rect.top == 430:
                            if theKillerBomb == None:
                                theKillerBomb = bomb
                                channel = pygame.mixer.find_channel(True)
                                if channel:
                                    #print "got channel"
                                    channel.play(enviro.soundEffect[Noise.MOTHER_HIT])
                                else:
                                    print "no channel for mother kill sound, will try to use main"
                                    enviro.soundEffect[Noise.MOTHER_HIT].play()                            
                                
                        if shieldPower > 0:
                            bomb.test(shieldSprite, "caught")                            
                                
                    if not theKillerBomb == None:
                        if not theKillerBomb.nuked:
                            theKillerBomb.paint()
                            theKillerBomb.nuke()
                        else:
                            alive = 0
                    
            for harvester in enviro.harvesters:
                harvester.getNextState(enviro.shields, 
                   enviro.theBase, enviro.generators, enviro.laser)
                
            for pad in enviro.padArray:
                pad.clearNeeds()

            next = enviro.you.moveYou(enviro.pads)
            if next == "up":
                enviro.you.aimUp(enviro.pads)
            elif next == "down":
                enviro.you.aimDown(enviro.pads)
            elif next == "right":
                enviro.you.aimRight(enviro.pads)
            elif next == "left":
                enviro.you.aimLeft(enviro.pads)
            elif next == "act":
                action = enviro.you.interact(enviro.generators, 
                           enviro.shields, enviro.theBase, enviro.laser)
                if action[0] > -1 and action[1] == 1:
                    enviro.doAction(enviro.you, action, enviro.gasGauges)

            autoTarget = False
            if not shooting:
                target = enviro.laser.autoTarget(bombList)            
                if target[0] > 0:
                    newCursor = target
                    shooting = True
                    autoTarget = True
            else:
                needHint = False
            if shooting:
                shooting = enviro.laser.shoot(bombList, newCursor, 
                                             releasedButton, autoTarget)
                if enviro.mother.state == "Hit":
                    sheIsDead = True

                    if pygame.mixer:
                        Noise.playMusic('JMICKEL_Allmyownworkv2.mp3')
                        motherBecameActive = False
                        
            if sheDied:
                sheDied = deadMother.paint()
                            
        if enviro.credits > 49999:
            alive=0
                    
        myClock.tick(30)
        
        if not paused:
            mainline.writeFPSandDifficulty(myClock, difficulty)

        console.draw()

        pygame.display.flip()
    
    pygame.mixer.music.fadeout(1000)    
    if enviro.credits > 49999:
        mainline.winner(difficulty)
    else:
        mainline.loser(bailoutCount)
        
        
        
if __name__ == '__main__':
    # Init the screen and sound and everything... 
    pygame.init()
    Noise.initMixer()
    myClock = pygame.time.Clock()
    enviro.screen = pygame.display.set_mode([800,600])
            
    pygame.display.set_caption('Produce, Defend, Win!')
    enviro.init()
    
    # Do the game until it is over...
    
    #import profile
    #profile.run('main(False, True)')
    main(False, True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    main(True, False)
                if event.key == pygame.K_r:
                    main(False, False)
                if event.key == pygame.K_q:
                    sys.exit()
                    
            if event.type == pygame.KEYDOWN:
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()                    
