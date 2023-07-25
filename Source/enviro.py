# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information

# Global stuff I need for my game environment
import YourStuff # needed here so I can test collisions...

from YourStuff import *
from AttackerStuff import *
from MotherShip import MotherShip
from GasFactory import GasFactory
from Laser import Laser
from Shields import Shields
from DeadFighter import DeadFighter
from Tile import Tile

import Noise

# There, this kludge will keep me from checking the code in with test mode
# enabled, provided I don't add AAAmytest.py to the repository :)
test = 0
testMenuSkip = 0
testEntryScreenSkip = 0
testing_modules = 0
try:
    from Source import AAAmytest
    test = AAAmytest.test
    testMenuSkip = AAAmytest.testMenuSkip
    testEntryScreenSkip = AAAmytest.testEntryScreenSkip
except ImportError:
    try:
        import AAAmytest
        test = AAAmytest.test
        testMenuSkip = AAAmytest.testMenuSkip
        testEntryScreenSkip = AAAmytest.testEntryScreenSkip
        testing_modules = 1
    except:
        #print "prod mode!"
        pass

""" GLOBAL variables """
""" First some static items we need to run the game:"""
# I was tearing my hair out before I thought of this easy, horrible solution!
if testing_modules:
    artPathHack = os.path.join('..','Graphics')
    soundPathHack = os.path.join('..','Sound')
else: # normal production mode
    artPathHack = os.path.join('Graphics')
    soundPathHack = os.path.join('Sound')

screen = 0
SHIELD_MAX = 2050 # this one is more of a hard-coded thing... determined from shield algorithm

# These are obsolete, need to clean them out now that I have good controls
effectsVolume = 2
        

genKeys = [ pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, 
            pygame.K_KP4, pygame.K_KP5, pygame.K_KP6,
            pygame.K_KP1, pygame.K_KP2, pygame.K_KP3]

map =   [ 
          [[-1,-1], [35,100], [100,100], [165,100], [230,100], [295,100], [360,100]],
          [[-1,-1], [35,230], [100,230], [165,230], [230,230], [295,230], [360,230]],
          [[-1,-1], [35,360], [100,360], [165,360], [230,360], [295,360], [360,360]],
          [[-1,-1], [-1,-1],  [-1,-1],   [-1,-1],   [-1,-1],   [-1,-1],   [360,540], [425,540], [545,540], [665,540]]
        ]

path = [ [[165,230], [100, 230], [100, 100], [35, 100],  [-1,-1]],
         [[165,230], [100, 230], [100, 100], [165, 100], [-1,-1]],
         [[165,230], [230, 230], [230, 100], [295, 100], [-1,-1]],
         
         [[165,230], [100, 230], [35,  230], [-1,-1]],
         [[165,230]],
         [[165,230], [230, 230], [295, 230], [-1,-1]],
         
         [[165,230], [100, 230], [100, 360], [35, 360], [-1,-1]],
         [[165,230], [100, 230], [100, 360], [165,360], [-1,-1]],
         [[165,230], [230, 230], [230, 360], [295,360], [-1,-1]],
        
         [[165,230], [230, 230], [230, 360], [360,360], [360,540], [425,540], [545,540], [-1,-1]], # to the shields
         [[165,230], [230, 230], [230, 360], [360,360], [360,540], [425,540], [660,540], [-1,-1]], # to the laser        
         [[165,230], [100,230], [-1,-1]], # stuck path 1
         [[165,230], [230,230], [-1,-1]], # stuck path 2
         [[165,230], [230, 230], [230, 360], [360,360], [360,540], [425,540], [435,540], [-1,-1]] # to the market        
        ]
        

soundEffect = []

padArray = []

tiles = []
        
pad_img = "pad1.png"
base_img = "base.png"
you_img = "man.png"
you_with_stuff_img = "manWithThing.png"
you_with_gas_img = "manWithGas.png"
factoryPad_img = "botFactoryPad.png"        
gasPad_img = "gasFactoryPad.png"

# http://python-vnc-viewer.googlecode.com/hg/vncviewer.py
LASER_POINTER = tuple([(24,24), (11,10)] + list(pygame.cursors.compile((
#012345678901234567890123
"        ..   ..         ", #0
"      ...X   X...       ", #1
"    ...XXX   XXX...     ", #2
"   ..XXXXX   XXXXX..    ", #3
"  ..XXXXXX   XXXXXX..   ", #4
" ..XXXXXXX   XXXXXXX..  ", #5
" .XXXXXXXX   XXXXXXXX.  ", #6
"..XXXXXXXX   XXXXXXXX.. ", #7
".XXXXXXXXX   XXXXXXXXX. ", #8
"                        ", #9
"                        ", #10
"                        ", #11
".XXXXXXXXX   XXXXXXXXX. ", #12
"..XXXXXXXX   XXXXXXXX.. ", #13
" .XXXXXXXX   XXXXXXXX.  ", #14
" ..XXXXXXX   XXXXXXX..  ", #15
"  ..XXXXXX   XXXXXX..   ", #16
"   ..XXXXX   XXXXX..    ", #17
"    ...XXX   XXX...     ", #18
"      ...X   X...       ", #19
"        ..   ..         ", #20
"                        ", #21
"                        ", #22
"                        ", #23
), 'X', '.'))) 

""" These need to be set to play, but only initialized at BOJ (not restart):"""
displayFPS = False
cheatKeys = False
combatStarted = True

if test == 1:
    INIT_MUSIC = 0
    INIT_EFFECTS = 50
    MOTHER_FLEET_INCREASE_WAITTIME = 1200
else:
    INIT_MUSIC = 50
    INIT_EFFECTS = 50
    MOTHER_FLEET_INCREASE_WAITTIME = 1200

MOTHER_START_POSITION = 810 # 810 is off the screen 
MOTHER_START_WAIT = 1800 # maybe 1500 for prod
MOTHER_RESTART_WAIT = 1000 # maybe 1000 for prod
MOTHER_BUILD_SPEED = 500 # maybe 500 for prod
MOTHER_LIFEGAIN_PER_LEVEL = 100 # greater gain <> greater fun
MOTHER_MIN_RESTART = 300

START_SHIELD_BAYS = [10,10,10]


BOMB_POWER = 500 

PRODUCTION_TIMER = 1 #20 is good for prod

FUEL_PER_PELLET = 80 # 80 good for prod
SHIELD_POWER_PER_CYCLE = 2 # 2 good for prod?

LASER_PER_PELLET = 50 # 5 may be good for prod?

LASER_UPGRADE_POWER = .75 

FIGHTER_LAUNCH_SPEED = 30.0 # maybe 30.0 good for prod? - be sure to float!

HARVESTER_COOLDOWN = 20

credits = 0

laserRefuelDisabled = False # pure testing this one

pads = pygame.sprite.Group()
fuelPile = []

you = 0
mother = 0
theBase = 0
factory = 0
shop = 0

gasGauges = []

shieldUpgrades = 1
laserUpgrades = 1
gasFactoryIsBuilt = False
botFactoryIsBuilt = False

gasFiles = ["gas-full.png", "gas-twoThirds.png", "gas-oneThird.png", "gas-empty.png"]
for gasFile in gasFiles:
    gas = GasGauge(gasFile)
    gasGauges.append(gas)
    
##fighterFile = "fighter.png"
##fighterFleet = []
##for i in range(0,9):
##    fighter = Fighter(fighterFile, len(fighterFleet))
##    fighterFleet.append(fighter) 
##    
    

""" Per-game, reinit on restart:"""
NEED_MONEY_TO_BUILD = True
#START_SHIELD_BAYS = [5,5,5]
START_SHIELD_POWER = 2050
SHIELD_COOLDOWN = 100
SHIELD_INCREASE_PER_CYCLE = 20 # unused? I forget what this meant...
LASER_POWER = 1.2
LASER_AIM_TIME = 100


def init():
    soundEffect.append(Noise.load_sound('3383__patchen__Rhino_09-cut.wav'))
    Noise.SHIELD_HIT = len(soundEffect) - 1
    soundEffect.append(Noise.load_sound('28917__junggle__btn107.wav'))
    Noise.BOMB_HIT = len(soundEffect) - 1
    soundEffect.append(Noise.load_sound('18387__inferno__lsax-stereo.wav'))
    Noise.LASER_MISS = len(soundEffect) - 1
    soundEffect.append(Noise.load_sound('36847__EcoDTR__LaserRocket2_trimmed.wav'))
    Noise.FIGHTER_KILLED = len(soundEffect) - 1
    soundEffect.append(Noise.load_sound('41525__Jamius__BigLaser_trimmed.wav'))
    Noise.FIGHTER_HIT = len(soundEffect) - 1 
    soundEffect.append(Noise.load_sound('6722_NoiseCollector_boom4.wav'))
    Noise.MOTHER_HIT = len(soundEffect) - 1    
    soundEffect.append(Noise.load_sound('25322_Therac_25_starshiphum.wav'))
    Noise.SHIELD_HUM = len(soundEffect) - 1
    soundEffect.append(Noise.load_sound('15350__Hell_s_Sound_Guy__PLASMA_RIFLE_ROUND_trimmed.wav'))
    Noise.MOTHER_SHOT = len(soundEffect) - 1 
    soundEffect.append(Noise.load_sound('63068__radian__odd_trimmedAndReworked.wav'))
    Noise.MOTHER_ENTERS = len(soundEffect) - 1 
    
    enviro.effectsVolumeController = Noise.Volume(enviro.screen,location=[42,570], size=[120,20], init=enviro.INIT_EFFECTS)    
    enviro.musicVolumeController = Noise.Volume(enviro.screen,location=[200,570], size=[120,20], init=enviro.INIT_MUSIC)
        
    for effect in enviro.soundEffect:
        effect.set_volume(enviro.effectsVolumeController.setting/100.0)     
    
    # This is way too slow... so we'll just put "tiles" for the parts that matter
    ##enviro.screen.blit(enviro.roadImage,[0,0])
    
    tileCoords = ((35,100,399,139), 
                  (35,230,399,269),
                  (35,360,399,399),
                  (100,140,139,399),
                  (230,140,269,399),
                  (360,140,399,579),
                  (400,540,704,579))
    
    theRoadImage = pygame.image.load(os.path.join(enviro.artPathHack,"road3.png")).convert_alpha()
    for coord in tileCoords:
        someTile = Tile(theRoadImage, coord[0], coord[1], coord[2], coord[3])
        enviro.tiles.append(someTile) 
        
    for i in range(0,11):
        fuelFile = "fuelStore" + str(i) + ".png"
        fuelState = FuelStuff(fuelFile)
        enviro.fuelPile.append(fuelState)  
        
    for location in range(0,9):
        coordX = enviro.getLocationX(location)
        coordY = enviro.getLocationY(location)
        if location == 0:
            enviro.factory = BotFactory(enviro.factoryPad_img, coordX, coordY, "needGrand0-white.png", "needGrand0.png", "needGrand1.png", "needGrand2.png", "needStuff.png", "botFactory.png")
            pad = enviro.factory
        elif location == 4:
            enviro.theBase = Base(enviro.base_img, coordX, coordY)
            pad = enviro.theBase
        elif location == 8:
            enviro.gasFactory = GasFactory(enviro.gasPad_img, coordX, coordY, 
               "needGrand0-white.png", 
               "needGrand0.png", 
               "needGrand1.png", 
               "needGrand2.png", 
               "needStuff.png", 
               "gasFactory.png")
            pad = enviro.gasFactory
        else:
            pad = Pad(location, enviro.pad_img, coordX, coordY, "pad1.png", "needGrand1-v2.png", "needGrand0-v2.png", "needStuff-v2.png")
        enviro.pads.add(pad)
        enviro.padArray.append(pad) 
        
    laserFile = "laser.png"
    enviro.laser = Laser(laserFile) 
    enviro.pads.add(laser) 
    
    shopFile = "market.png"    
    enviro.shop = Shop(shopFile, 400, 450)
    enviro.pads.add(shop)
    
    shieldsFile = "shields.png"
    shieldsIncreasingFile = "shieldsUp.png"
    enviro.shields = Shields(shieldsFile, shieldsIncreasingFile, enviro.START_SHIELD_BAYS)
    enviro.pads.add(enviro.shields)               
        
                       


# Get the game going... create and paint the generator pads, the base, you, etc...
def start(difficulty):
    
    if difficulty == "Easy":
        enviro.combatStarted = False
        
    enviro.screen.fill((0,0,0)) # love the black screen
    
    enviro.harvesters = []
    enviro.generators = []
    
    if test == 1:
        enviro.START_SHIELD_POWER = 2000
        
        enviro.MOTHER_START_WAIT = 10 # maybe 1000 for prod
        enviro.MOTHER_START_POSITION = 710 # 810 is off the screen
        enviro.MOTHER_BUILD_SPEED = 50 
        enviro.MOTHER_FLEET_INCREASE_WAITTIME = 10 
        enviro.MOTHER_RESTART_WAIT = 10  
        enviro.MOTHER_MIN_RESTART = 10
        
        enviro.LASER_AIM_TIME = 10000 # 10 gets all as long as there is power, 20 all but a few
        
        enviro.SPEED = 5
        enviro.YOURSPEED = 20
        
        #enviro.LASER_POWER = 1000
        enviro.shieldUpgrades = 1
        enviro.laserUpgrades = 10
        
        enviro.credits = 0
    else:

        enviro.START_SHIELD_POWER = 1000
        
        enviro.BOMB_POWER = 500
        enviro.LASER_POWER = 1.2
        enviro.LASER_AIM_TIME = 100
        
        enviro.SPEED = 5
        enviro.YOURSPEED = 5
        enviro.MOTHER_BUILD_SPEED = 500
    
    enviro.shields.fuelBay = [10,10,10] # argh I'm tired of flailing, just do this   
    enviro.laser.fuelBay = [10,10,10]
    
    enviro.shields.initUpgrades()
    enviro.laser.initUpgrades()

    if enviro.combatStarted:
        for pad in enviro.pads:
            pad.paintPad()
        # this is already painted but whatever...
        enviro.gasFactory.paintPad()
        enviro.factory.paintPad()
        enviro.laser.paint([640,450], enviro.fuelPile) 
        enviro.shop.paint()
        enviro.shields.paint([520,450], enviro.fuelPile)
        
    #enviro.roadImage = pygame.image.load("road3.png").convert_alpha()
        
    enviro.you = You(enviro.you_img,enviro.you_with_stuff_img,enviro.you_with_gas_img, [0,0] )
    enviro.you.moveYou(enviro.pads) # get you drawn on the screen
    
    enviro.theBase.fuelBay = [0,0,0]    
    enviro.theBase.paint(enviro.fuelPile)
    
    fighterFile = "fighter.png"
    fighterFleet = []
    for i in range(0,9):
        fighter = Fighter(fighterFile, len(fighterFleet))
        fighterFleet.append(fighter) 
            
        
    # epic effort to get a dying fighter properly animated...
    fighterDeathFileName = "deadFighter10PxA-"
    enviro.deadFighterModel = DeadFighter(fighterDeathFileName)

    motherShipFile = "mother.png"
    bomb_image = "bomb.png"
    enviro.mother = MotherShip(motherShipFile, fighterFleet, bomb_image)
    
    enviro.screen.blit(pygame.image.load(os.path.join(enviro.artPathHack,"effectsIcon.png")), [10,570])
    enviro.screen.blit(pygame.image.load(os.path.join(enviro.artPathHack,"musicIcon.png")), [170,570])

    paintRoadTiles()
    
    enviro.fleetMax = enviro.mother.getFleetSize()
    if difficulty == "Easy":
        enviro.fleetMax = 5
    
    if difficulty == "Hard" or difficulty == "Very Hard":
        enviro.NEED_MONEY_TO_BUILD = True
    else:
        enviro.NEED_MONEY_TO_BUILD = False
       
 
    # How much more does it cost per upgrade to shoot?
    if difficulty == "Easy":
        enviro.LASER_COST_FACTOR = .5
        enviro.PRODUCTION_TIMER = 1
    elif difficulty == "Normal":
        enviro.LASER_COST_FACTOR = 1
        enviro.PRODUCTION_TIMER = 3
    elif difficulty == "Hard":
        enviro.LASER_COST_FACTOR = 1.5
        enviro.PRODUCTION_TIMER = 10
    else:
        enviro.LASER_COST_FACTOR = 2
        enviro.PRODUCTION_TIMER = 20


def paintRoadTiles():
    for t in enviro.tiles:
        t.paint(enviro.screen)
        
def writeCredits(credits):
    creds = "Credits: $" + str(credits)
    font = pygame.font.Font(None, 20)
    creds_text = font.render(creds, 1, (255,255,255))
    creds_pos = [10, 550]
    pygame.draw.rect(enviro.screen, [0,0,0], [10,550,200,20], 0)
 
    enviro.screen.blit(creds_text, creds_pos)

# Translate screen locations into screen coordinates
def getLocationX(location):
    coordX = 0
    if (location == 0 or location == 3 or location == 6):
        coordX = 10 
    if (location == 1 or location == 4 or location == 7):
        coordX = 140
    if (location == 2 or location == 5 or location == 8):
        coordX = 270
    return coordX

def getLocationY(location):
    coordY = 0
    
    if (location == 0 or location == 1 or location == 2):
        coordY = 10 
    if (location == 3 or location == 4 or location == 5):
        coordY = 140
    if (location == 6 or location == 7 or location == 8):
        coordY = 270
    return coordY
     
    


# Test sprite collision between "you" and the "pads"
def testCollision(you, testSpeed, pads):
    testYou = YourStuff.You(you.theImage,you.theImage,you.theImage,testSpeed)
    testYou.rect.top = you.rect.top
    testYou.rect.right = you.rect.right
    testYou.rect = testYou.rect.move(testYou.speed)
    if pygame.sprite.spritecollideany(testYou, pads):
        #print "collide!"
        #print pygame.sprite.spritecollideany(testYou, pads)
        return 1
    return 0



                    

    
def writePaused(isPaused):
    if isPaused:
        screenDisplaySurface = pygame.display.get_surface()
        enviro.screenCopy = screenDisplaySurface.copy()
        
        pauseImage = pygame.image.load(os.path.join(enviro.artPathHack,"pauseInstructions.png")).convert()
        enviro.screen.blit(pauseImage,[0,0])
        
##        font = pygame.font.Font(None, 20)
##        instruction_text = font.render("***PAUSED***", 1, (255,255,255))
##        enviro.screen.blit(instruction_text, [100,480])
        
    else:
        pygame.draw.rect(enviro.screen, [0,0,0], [100,480,200,20], 0)
        enviro.screen.blit(enviro.screenCopy,[0,0])
    pygame.display.flip()
 
def intlist(a):
    return [int(x) for x in a]

# http://www.pygame.org/docs/ref/draw.html#pygame.draw.circle   
def drawcircle(image, colour, origin, radius, width=0):
    if width == 0:
        pygame.draw.circle(image,colour,intlist(origin),int(radius))
    else:
        if radius > 65534/5: radius = 65534/5
        circle = pygame.Surface([radius*2+width,radius*2+width]).convert_alpha()
        circle.fill([0,0,0,0])
        pygame.draw.circle(circle, colour, intlist([circle.get_width()/2, circle.get_height()/2]), int(radius+(width/2)))
        if int(radius-(width/2)) > 0: pygame.draw.circle(circle, [0,0,0,0], intlist([circle.get_width()/2, circle.get_height()/2]), abs(int(radius-(width/2))))
        image.blit(circle, [origin[0] - (circle.get_width()/2), origin[1] - (circle.get_height()/2)])  
    
# Do an action - connections "you" to "generators"    
def doAction(you, action, gasGauges):
    #print "doing ACTION at ", action[0], "act=", action[1]
    if action[0] > -1 and action[1] == 1:
        foundGen = False
        for generator in generators:
            if generator.location == action[0]:
                foundGen = True
                # There's a generator here, does it have stuff? if so, get it
                if generator.isReady and you.carrying == 0:
                    #print "Get the stuff"
                    you.carrying = 1
                    generator.harvestStuff()
                else:
                    if you.carrying == 2:
                        generator.refill(gasGauges)
                        you.carrying = 0
                        
        if not foundGen:
            if enviro.padArray[action[0]].padPainted:
                if you.carrying <> 1:
                    enviro.padArray[action[0]].needStuff()
                else:
                    if enviro.NEED_MONEY_TO_BUILD and not enviro.credits > 999:
                        enviro.padArray[action[0]].needMoney()
                    else:
                        #print "You bought a generator!"
                        enviro.padArray[action[0]].needCount = 0
                        newGen = Generator(action[0], gasGauges, "generator0.png")
                        generators.append(newGen)
                        you.carrying = 0
                        if enviro.NEED_MONEY_TO_BUILD:
                            enviro.credits = enviro.credits - 1000
                            enviro.writeCredits(enviro.credits)

                            
        
if __name__ == '__main__':
    
    print "TEST: winner"
    pygame.init()
    enviro.screen = pygame.display.set_mode([800,600])
    myClock = pygame.time.Clock()
    
    winner()            
    while True:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if (event.type == pygame.KEYDOWN):
            if (pygame.key.get_mods() == 1024): # command key
                if (event.key == 113):   # q
                    sys.exit()
                    
        myClock.tick(30)
        pygame.display.flip()                                           