# coding=UTF8
# Copyright © 2010 Rob Leachman
# Please see the file COPYING in this distribution for license information
import enviro
import pygame

def fps(display=True):
    '''\
    Display frames per second
    Parameters:
       display - True=do display, False=don't display
    '''
    
    enviro.displayFPS = display
    
def cheat(doCheats=True):
    '''\
    Enable cheat keys
    Parameters:
       display - True=allow cheats, False=no cheating
    '''
    
    enviro.cheatKeys = doCheats

def credits(n):
    '''\
    Cheat - set credits
    Parameters:
       n - Number of credits to add
    '''
    
    enviro.credits += n
    enviro.writeCredits(enviro.credits)
    return "added %d credits" % n

# I left this in for grins
def line(start_pos, end_pos, color=[0,0,0], width=1):
	'''\
	Call pygame.draw.line
	Parameters:
		start_pos - x,y coordinate of start point
		end_pos - x,y coordinate of end point
		color - Line color in RGB format
		width - Line thickness 
	'''
	pygame.draw.line(enviro.screen, color, start_pos, end_pos, width)
