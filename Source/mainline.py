# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import pygame
import sys

import enviro
from MenuClass import cMenu, EVENT_CHANGE_STATE
from Harvester import Harvester
from Generator import Generator
from GasFactory import GasFactory # for testing
import gradients
import mainline # seems wacky but we need it for getattr on functions located here

# Less interesting mainline functions

textPos = 10

def startCombat():
    enviro.combatStarted = True
    enviro.laser.paint([640,450], enviro.fuelPile)
    enviro.shields.paint([520,450], enviro.fuelPile)
    for pad in enviro.pads:
        if pad.location <> 0 and pad.location <> 4 and pad.location <> 8 and pad.location < 9:
            foundGen = False
            for generator in enviro.generators:
                if generator.location == pad.location:
                    foundGen = True
            if not foundGen:
                pad.paintPad()
    writeInstructions("Ready to rock!")                

def cheatKeys(key):
    """ this was great for development """
    genLocation = enviro.genKeys.index(key)
    
    if (genLocation == 4): # the base, add a harvester
        harvCount = len(enviro.harvesters)
        if (harvCount < 10):
            newHarv = Harvester(len(enviro.harvesters))
            enviro.harvesters.append(newHarv)
        else:
            print "Max 10 harvesters!"
    else: # a producing location, add a generator
        foundGen = False
        for generator in enviro.generators:
            if generator.location == genLocation:
                foundGen = True
        if (foundGen == False):
            newGen = Generator(genLocation, enviro.gasGauges, "generator0.png")
            enviro.generators.append(newGen) 
            
# http://diveintopython.org/power_of_introspection/index.html
def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    
    Takes module, class, list, dictionary, or string."""
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join(["%s %s" %
                      (method.ljust(spacing),
                       processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])
                
# I needed something like info, to dump my variables and be sure reset works as expected
def varInfo(object, spacing=10, collapse=1):
    methodList = [method for method in dir(object) if not callable(getattr(object, method))]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    result = ""
    for method in methodList:
        if method <> "__builtins__" and method <> "THECOLORS":
        #result = result.join("%s %s" % (method.ljust(spacing), processFunc(str(getattr(object, method)))))
            result += method.ljust(spacing) + " = " 
            result += processFunc(str(getattr(object, method)))
            result += "\n"
    print result            
               

def writeInstructions(difficulty):
    pygame.draw.rect(enviro.screen, (0,0,0), [10,480,300,70], 0)
    instruction = "Arrow keys or WASD to move, space to act"
    font = pygame.font.Font(None, 20)
    instruction_text = font.render(instruction, 1, (255,255,255))
    instruction_pos = [10, 500]
    enviro.screen.blit(instruction_text, instruction_pos)
    if difficulty == "Easy":
        instruction_text = font.render("Your goal is to complete the tutorial", 1, (255,255,255))
    else:
       instruction_text = font.render("Your goal is to make $50000", 1, (255,255,255))
    enviro.screen.blit(instruction_text, [10,520])
    # inverse text:
    # instruction_text = font.render("Hit <Esc> to pause, ctrl-q to quit, mouse to shoot", 1, (0,0,0), (255,255,255))
    instruction_text = font.render("Hit <Esc> to pause, ctrl-q to quit, mouse to shoot", 1, (255,255,255))
    enviro.screen.blit(instruction_text, [10,480]) 
    
    if difficulty == "Easy":
        writeText("clear");
        text = "Hey first, thanks for playing! Let's see what you're in for:"
        writeText(text)
        writeText("See the generator produce some green ""stuff""?")
        writeText("");
        writeText("Go get it, use the right arrow key to move,")
        writeText("and then spacebar to collect the stuff.")
        
#World's worst debugging method, I need to find something good for OS X        
##    pygame.display.flip()
##    foo = raw_input("foo")

def writeHelpfulHintLine(linePainted):
    # Could try for inverse... but just a nice underline will hopefully do...
    # NOPE TOO SUBTLE
    font = pygame.font.Font(None, 20)
    whiteHint = font.render("mouse to shoot", 1, (255,0,0), (255,255,255))
    blackHint = font.render("mouse to shoot", 1, (255,255,255), (0,0,0))
    if linePainted:
        #pygame.draw.lines(enviro.screen, [0,0,0], False, [[244,492],[352,492]], 1)
        enviro.screen.blit(blackHint, [244,480])
        return False
    #pygame.draw.lines(enviro.screen, [255,255,255], False, [[244,492],[352,492]], 1)
    enviro.screen.blit(whiteHint, [244,480])
    return True
        
def demoMode(demoStep, bailoutCount, alive): 
    advance = False
    
    findSomebodyToBlame = False
    for generator in enviro.generators: # only 1
        if generator.checkTankEmpty() and not generator.isReady: 
            findSomebodyToBlame = True
    if enviro.you.carrying == 0 and findSomebodyToBlame and not enviro.theBase.hasStuff():
        harvesterCarryingThing = False # least important bug ever, but I squashed it
        for harvester in enviro.harvesters: # only one of these too
            if harvester.state == "Carrying":
                harvesterCarryingThing = True
        if not harvesterCarryingThing:
            if bailoutCount < 2:
                mainline.writeText("")
                mainline.writeText("You're stuck, so the government bailed you out!")
                mainline.writeText("")
                mainline.writeText("Now read the instructions and")
                mainline.writeText("finish the tutorial!")                    
                enviro.theBase.stashStuff()
                bailoutCount += 1
            else:
                alive = 0

        
    if demoStep == 0 and enviro.you.carrying == 1:
        advance = True
    elif demoStep == 1 and enviro.theBase.hasStuff():
        advance = True
    elif demoStep == 2:
        for generator in enviro.generators: # only 1
            if generator.checkTankEmpty(): 
                advance = True
                enviro.shop.paint()
    elif demoStep == 3 and enviro.credits > 0:
            advance = True
    elif demoStep == 4:
        for generator in enviro.generators: # only 1
            if generator.isReady == False:
                enviro.gasFactory.paintPad()
                advance = True
    elif demoStep == 5 and enviro.gasFactory.built == 1:
        advance = True
    elif demoStep == 6 and enviro.you.carrying == 2:
        advance = True
    elif demoStep == 7 and enviro.you.carrying == 0:
        enviro.factory.paintPad()
        advance = True
    elif demoStep == 8 and enviro.factory.built == 1:
        advance = True
    elif demoStep == 9 and len(enviro.harvesters) > 0:
        advance = True                    
    if advance:
        demoStep += 1
        nextDoc = getattr(mainline, "writeStep%s" % demoStep)
        nextDoc()
    # sheesh all I  did was move this from main... now look at this mess:
    return [demoStep, bailoutCount, alive]
            
def writeStep1():
    writeText("clear");
    writeText("Super! You can store stuff at the base.")
    writeText("");
    writeText("Do that now, left arrow to move back and then")
    writeText("spacebar to drop the stuff.")
    
def writeStep2():
    writeText("clear");
    writeText("You are doing fine!")
    writeText("");
    writeText("Go get the next box of stuff from the generator.")
    
def writeStep3():
    writeText("clear");
    writeText("Perfect!")
    writeText("");
    writeText("You can sell stuff at the market.")
    writeText("");
    writeText("Take your stuff down there and sell it.") 
    
def writeStep4():
    writeText("clear");
    writeText("Whoohoo you've got some money!")
    writeText("");
    writeText("Next let's see about gas. Go get the next box")
    writeText("of stuff from the generator and see what happens.")
    
def writeStep5():
    writeText("clear");
    writeText("Oh no!")
    writeText("");
    writeText("The generator isn't producing because it is out of gas.")
    writeText("");    
    writeText("Fortunately there's a gas factory nearby...") 
    writeText("or rather, there could be, you need to build it.")     
    writeText("");    
    writeText("Use a block of stuff to build the gas factory.") 
    
def writeStep6():
    writeText("clear");
    writeText("That's it!")
    writeText("");
    writeText("Now you can turn stuff into fuel.")
    writeText("");    
    writeText("Grab a block of stuff and get some gas...")

def writeStep7():
    writeText("")
    writeText("and then take it to the generator.")
    
def writeStep8():
    writeText("clear");
    writeText("There you go!")
    writeText("");
    writeText("OK that is how you do it. Make stuff, sell stuff,")
    writeText("keep your generators fueled up and producing.")    
    writeText("");
    writeText("Fun, but doing that over and over would get old fast.")
    writeText("");
    writeText("Let's build robots to do the work for us!")
    writeText("Take some stuff and build the robot factory.")
    
def writeStep9():
    writeText("clear");
    writeText("Right on!")
    writeText("");
    writeText("Can you guess what's next? I knew you could!")
    writeText("Take some stuff and build your first robot.")
    
def writeStep10():
    writeText("clear");
    writeText("Excellent!")
    writeText("");
    writeText("Enough tutorial, you can figure out the rest.")
    writeText("");
    writeText("Hit the <Esc> key to pause the game now and")
    writeText("view the other clues... and you'll be ready")
    writeText("to start! Have fun!")
        
def writeText(text):
    global textPos
    
    if text == "clear":
        textPos = 10
        pygame.draw.rect(enviro.screen, (0,0,0), [400,0,400,449],0)
    else:
        font = pygame.font.Font(None, 20)
        textOut = font.render(text, 1, (255,255,255))
        enviro.screen.blit(textOut, [400, textPos])
        textPos += 20
    
    
def writeFPSandDifficulty(myClock, difficulty):
    fps = int(myClock.get_fps())
    font = pygame.font.Font(None, 20)
    if enviro.displayFPS == True:
        fpsText = "FPS=%d Difficulty=%s" % (fps, difficulty)
        #print fps
    else:
        fpsText = "Difficulty=%s" % (difficulty)
    fpsOut = font.render(fpsText, 1, (255,255,255))
    pygame.draw.rect(enviro.screen, (0,0,0), [10,460,200,20], 0)
    enviro.screen.blit(fpsOut, [10,460])    

def menu():
    #enviro.screen.fill((0,0,0)) # love the black screen
    enviro.screen.blit(gradients.vertical_func((800,600), (128,128,128), (0,0,0)), (0,0))
    
    menu = cMenu(50, 50, 20, 5, 'vertical', 100, enviro.screen,
               [('Easy - Instruction Mode', 1, None),
                ('Normal',  2, None),
                ('Hard', 3, None),
                ('Very Hard', 4, None),
                ('Options', 5, None)])
    optionsMenu = cMenu(50, 50, 20, 5, 'vertical', 100, enviro.screen,
               [('Full Screen', 6, None),
                ('Window Screen',  7, None)])
                
    menu.set_center(True, True)
    menu.set_alignment('center', 'center')
    #menu.set_refresh_whole_surface_on_load(True)
    state = 0
    prev_state = 1
    rect_list = []
    #pygame.event.set_blocked(pygame.MOUSEMOTION) -- WORKS WITH MOUSE NOW!
    
    
    # Default -- added to his menu class, to set the choice to more than top of menu
    menu.initialSelection = 1
    
    difficulty = "unchosen"
    # Menu loop
    while difficulty == "unchosen":
        # Check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state
            font = pygame.font.Font(None, 20) 
            instruction_text = font.render("Select difficulty (up/down arrows and enter, or mouse)", 1, (255,255,255))
            enviro.screen.blit(instruction_text, [10,480])
            pygame.display.flip()

        # Get the next event
        e = pygame.event.wait()

        # Update the menu, based on which "state" we are in - When using the menu
        # in a more complex program, definitely make the states global variables
        # so that you can refer to them by a name
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE or e.type == pygame.MOUSEBUTTONUP or pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEMOTION:
         if state == 0:
            menu.redraw_all()
            rect_list, state = menu.update(e, state)
         elif state == 1:
            difficulty = "Easy"
            state = 0
         elif state == 2:
            difficulty = "Normal"
            state = 0
         elif state == 3:
            difficulty = "Hard"
            state = 0
         elif state == 4:
            difficulty = "Very Hard"
            state = 0
         elif state == 5:
            rect_list, state = optionsMenu.update(e, state)
         elif state == 6:
            # Full-screen mojo from Arcade Tonk Tanks!
            setFullscreen()
##            screenrect = pygame.Rect(0, 0, 800, 600) 
##            bestdepth = pygame.display.mode_ok(screenrect.size, pygame.FULLSCREEN, 32)
##            enviro.screen = pygame.display.set_mode(screenrect.size, pygame.FULLSCREEN, bestdepth)
            state = 0
         elif state == 7:
            setWindowed()
##            enviro.screen = pygame.display.set_mode([800,600])
            state = 0
         else:
            print 'never-never land'
            pygame.quit()
            sys.exit()

        # Quit if the user presses the exit button
        if e.type == pygame.QUIT:
         pygame.quit()
         sys.exit()

        # Update the screen
        pygame.display.update(rect_list)
        
    # Did menu
    #pygame.event.set_allowed(pygame.MOUSEMOTION)
    return difficulty

def setFullscreen():
    screenrect = pygame.Rect(0, 0, 800, 600) 
    bestdepth = pygame.display.mode_ok(screenrect.size, pygame.FULLSCREEN, 32)
    enviro.screen = pygame.display.set_mode(screenrect.size, pygame.FULLSCREEN, bestdepth) 
    enviro.screen.blit(gradients.vertical_func((800,600), (128,128,128), (0,0,0)), (0,0))    
    
def setWindowed():
    enviro.screen = pygame.display.set_mode([800,600])

def loser(bailouts):
    #enviro.screen.fill([0,0,0]) 
    enviro.screen.blit(gradients.vertical_func((800,600),(200,200,200),(255,0,0)), (0,0))
    enviro.screen.blit(gradients.vertical_func((600,200),(255,255,255),(128,128,128)), (100,200))
    #loser = "LOSER" #funny stuff!
    loser = "YOU LOST"
    font = pygame.font.Font(None, 160)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [115, 210]
    enviro.screen.blit(loser_text, loser_pos)
    
    hint1 = "HINT: try harder?"
    if bailouts > 1:
        hint1 = "HINT: the government went bankrupt, try again!"
        font = pygame.font.Font(None, 20)
        loser_text = font.render(hint1, 1, (0,0,0))
        loser_pos = [210, 320]
        enviro.screen.blit(loser_text, loser_pos)    
    elif enviro.gasFactory.built == 0:
        hint1 = "HINT: the generators need to be refueled and you didn't buy a gas station"
        font = pygame.font.Font(None, 20)
        loser_text = font.render(hint1, 1, (0,0,0))
        loser_pos = [160, 320]
        enviro.screen.blit(loser_text, loser_pos)
    elif len(enviro.harvesters) == 0:
        hint1 = "HINT: bots are your friends but you built no bots"
        font = pygame.font.Font(None, 20)
        loser_text = font.render(hint1, 1, (0,0,0))
        loser_pos = [210, 320]
        enviro.screen.blit(loser_text, loser_pos)            

    loser = "You are a loser this time, thanks for trying!"
    font = pygame.font.Font(None, 20)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [268, 340]
    enviro.screen.blit(loser_text, loser_pos)                   
    
    loser = "Hit c to continue, r to restart, q to quit"
    font = pygame.font.Font(None, 20)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [295, 360]
    enviro.screen.blit(loser_text, loser_pos)
    pygame.display.flip()  
        
def winner(difficulty):
    #enviro.screen.fill((0,0,0))
    enviro.screen.blit(gradients.vertical_func((800,600),(200,200,200),(0,0,255)), (0,0))
    #pygame.draw.rect(enviro.screen, [255,255,255], [100,200,600,200], 0)
    enviro.screen.blit(gradients.vertical_func((600,200),(255,255,255),(128,128,128)), (100,200))
    loser = "WINNER!"
    font = pygame.font.Font(None, 160)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [150, 210]
    enviro.screen.blit(loser_text, loser_pos)
    
    loser = "You are AWESOME, thanks for playing!"
    font = pygame.font.Font(None, 20)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [268, 320]
    enviro.screen.blit(loser_text, loser_pos) 
    
    if difficulty == "Very Hard":
        hint1 = "Wow you did it, beat the hardest level, excellent!"
    else:
        hint1 = "You beat the \"%s\" level, can you do even better?" % difficulty
    font = pygame.font.Font(None, 20)
    loser_text = font.render(hint1, 1, (255,0,0))
    loser_pos = [210, 340]
    enviro.screen.blit(loser_text, loser_pos)                       
    
    loser = "Hit r to restart, q to quit"
    font = pygame.font.Font(None, 20)
    loser_text = font.render(loser, 1, (0,0,0))
    loser_pos = [285, 360]
    enviro.screen.blit(loser_text, loser_pos)  
    pygame.display.flip()
    

if __name__ == '__main__':
    
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    delay=100
    interval=50
    pygame.key.set_repeat(delay,interval)
    
# stuff needed for init:
    enviro.gasFactory = GasFactory("gasFactoryPad.png", 0,0, 
               "needGrand0-white.png", 
               "needGrand0.png", 
               "needGrand1.png", 
               "needGrand2.png", 
               "needStuff.png", 
               "gasFactory.png")
            
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif (event.type == pygame.KEYDOWN):
                if (pygame.key.get_mods() == 1024): # command key
                    if (event.key == 113):   # q
                        sys.exit()
                        
                if event.key == pygame.K_SPACE:
                    loser(0)
                if event.key == pygame.K_x:
                    winner("Easy")                    
        
        myClock.tick(30)
        pygame.display.flip()      