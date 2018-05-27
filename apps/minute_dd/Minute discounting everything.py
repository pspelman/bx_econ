#!/usr/bin/env python

##
## Micky Koffarnus made this (Jan 2014)
##


import csv
import pygame
from random import choice, shuffle, random
import VisionEgg
VisionEgg.start_default_logging(); VisionEgg.watch_exceptions()
from VisionEgg.Core import *
from VisionEgg.FlowControl import Presentation, Controller, FunctionController
from VisionEgg.MoreStimuli import *
from VisionEgg.Textures import *
import pygame
import OpenGL.GL as gl
from VisionEgg.DaqKeyboard import *
from VisionEgg.Text import *
from VisionEgg.Textures import *
import Image, ImageDraw # Python Imaging Library (PIL)
import sys

NEW_BLOCK_TIME=5

if len(sys.argv)<8:
    print ' '
    sid = raw_input('Subject ID: ')
    exp = raw_input('Session: ')
    commodity = raw_input('Commodity with unit (e.g., "g of cocaine"). \n     Just put $ for money: ')
    amount = float(raw_input('Delayed or probabilistic amount: '))
    probability = int(raw_input('Delay [0] or probabilistic [1] discounting: '))
    losses = int(raw_input('Gains [0] or losses [1]: '))
    if probability==0:
        past = int(raw_input('Future [0] or past [1] events: '))
    else:
        past = 0
    explicit0 = int(raw_input('Implicit [0] or explicit [1] zero: '))
    social = int(raw_input('Individual [0], Social Me-Me [1], Social Me-We [2], \n     Social We-Me [3], Social We-We [4] discounting: '))
else:
    sid = sys.argv[1]
    exp = sys.argv[2]
    commodity = sys.argv[3]
    amount = float(sys.argv[4])
    probability = int(sys.argv[5])
    losses = int(sys.argv[6])
    past = int(sys.argv[7])
    explicit0 = int(sys.argv[8])
    if len(sys.argv)==10:
        social = int(sys.argv[9])
    else:
        social=0

tr_len = 2

x1=range(1,5,1)
x2=[f/2.0 for f in x1]
isi_array=[choice(x2) for i in range(4)]

trs=4*tr_len+sum(isi_array)*2 # 5 questions
gn_sec_n=trs*tr_len # total time for presentation
gn_keystroke = 0
question=0
qIndex=1
screenText=['','']
screenText2=['','']
k=0
ed50=0
subQ=-1
krow=0
blocknum=0
# log file name
if not os.path.exists('data'):
    os.makedirs('data')    
if not os.path.exists('data\%s' % (sid)):
    os.makedirs('data\%s' % (sid))
log_filename = 'data\%s\MinuteDisc_%s_%s_' % (sid, sid, exp) + time.strftime ('%m-%d-%Y_%Hh-%Mm-%Ss.csv')
shuffle(isi_array)
isi_array=[0]+isi_array # no delay before first question
isi = 0
isi_index=0
now=1
firsttime=0
response=0
stim_onset=0
fixon=0
newseton=0
taskendon=0
goodrow = []
fontsize = 60
if len(commodity)>15: fontsize=40
if len(commodity)>25: fontsize=30
amtText=['','']
amtText0=''

# Read/write data files
# firstFiveFile is arranged by tree level -- e.g, 1,2,2,3,3,3,3,etc.
if probability==1:
    firstFiveFile = csv.reader(open('probabilities.dat','rU'))
else:
    firstFiveFile = csv.reader(open('delays.dat','rU'))
logfile=open(log_filename,'w')
logfile.write("Date,Time,Commodity,Amount,Task type,Amount sign,Time sign,Zero\n")
logfile.write(time.strftime ('%m-%d-%Y,%H:%M:%S') + ",%s,%3.2f" % (commodity, amount))
if probability==1: 
    logfile.write(",Probability disc")
else:
    logfile.write(",Delay disc")
if losses==1: 
    logfile.write(",Losses")
else:
    logfile.write(",Gains")
if past==1: 
    logfile.write(",Past")
elif probability==1:
    logfile.write(",Present")
else:
    logfile.write(",Future")
if explicit0==1: 
    logfile.write(",Explicit")
else:
    logfile.write(",Implicit")
if social==0: 
    logfile.write(",Individual\n\n")
elif social==1:
    logfile.write(",Social Me-Me\n\n")
elif social==2:
    logfile.write(",Social Me-We\n\n")
elif social==3:
    logfile.write(",Social We-Me\n\n")
elif social==4:
    logfile.write(",Social We-We\n\n")
if probability==1:
    logfile.write("Question,Stim onset,Response time,Amount,Delay,Response [0P;1C],Imm Loc [0L;1R]\n")
else:
    logfile.write("Question,Stim onset,Response time,Amount,Delay,Response [0D;1I],Imm Loc [0L;1R]\n")

# Viewport parameters
import ctypes
user32 = ctypes.windll.user32
if user32.GetSystemMetrics(0) < 1024:
    print " "
    print "Horizontal screen resolution needs to be at least 1024."
    raw_input("Press enter to exit")
    sys.exit()    
screen=VisionEgg.Core.Screen(size=(user32.GetSystemMetrics(0),user32.GetSystemMetrics(1)),fullscreen=True)
screen.parameters.bgcolor = (0.0,0.0,0.0,0.0)
d_screen_half_x = screen.size[0]/2
d_screen_half_y = screen.size[1]/2

# Vision Egg objects

title = Text(text='Please choose the option you prefer in each case.',
        color=(1.0,1.0,1.0),
        position=(d_screen_half_x,d_screen_half_y+120),
        font_size=60,
        anchor='center')
		
title2 = Text(text='Press 5 to continue.',
        color=(1.0,1.0,1.0),
        position=(d_screen_half_x,d_screen_half_y+60),
        font_size=60,
        anchor='center')

newset = Text(text='NEW SET',
        color=(1.0,1.0,1.0),
        position=(d_screen_half_x,d_screen_half_y+120),
        font_size=60,
        anchor='center')

left_choice = Text(text=' ',
              color=(1.0,1.0,1.0),
              position=(d_screen_half_x/2,d_screen_half_y+fontsize),
              font_size=fontsize,
              anchor='center')

left_choice2 = Text(text=' ',
              color=(1.0,1.0,1.0),
              position=(d_screen_half_x/2,d_screen_half_y),
              font_size=fontsize,
              anchor='center')


right_choice = Text(text=' ',
              color=(1.0,1.0,1.0),
              position=(d_screen_half_x+(d_screen_half_x/2),d_screen_half_y+fontsize),
              font_size=fontsize,
              anchor='center')
              
right_choice2 = Text(text=' ',
              color=(1.0,1.0,1.0),
              position=(d_screen_half_x+(d_screen_half_x/2),d_screen_half_y),
              font_size=fontsize,
              anchor='center')

fixation = FixationCross(on = True, position=(d_screen_half_x, d_screen_half_y),size=(64,64))

taskend = Text(text='Task Complete',
          color=(1.0,1.0,1.0),
          position=(d_screen_half_x,d_screen_half_y+120),
          font_size=80,
          anchor='center')

viewportIntro = Viewport(screen=screen)
viewport = Viewport(screen=screen, stimuli=[title, title2, left_choice, right_choice, left_choice2, right_choice2, fixation, newset, taskend])

p = Presentation(
    go_duration = (2000,'seconds'), # run for longer than needed
    trigger_go_if_armed = 0, #wait for trigger
    viewports = [viewport,viewportIntro])

# Store first five questions in array
firstFive=[]    # store first five questions in this array
for i in range(5):
    firstFive.append([])
    for j in range(2**i):
        firstFive[i].append(firstFiveFile.next()) 

def getState(t):
    global qIndex, screenText, screenText, amtText, amtText0, k, question, gn_keystroke, subQ, amountRow, delay, krow, blocknum
    global isi, isi_index, now, firsttime, response, stim_onset, fixon, newseton, goodRow, taskendon

    if (t > isi+isi_array[isi_index]):
        newseton=0
        fixon=0
        taskendon=0
        if firsttime: 
            now = int(round(random()))
            stim_onset=t
            firsttime=0
        
        #### Ask first 5 questions
        if question < 5:
            delay = firstFive[question][qIndex-1][0]
            if commodity=='$':
                amtText0 = "$0"
                if amount<1000:
                    amtText[now] = "$%3.2f" % (float(amount/2))
                    amtText[1-now] = "$%3.2f" % (amount)
                else:
                    amtText[now] = "$%s" % (group(int(amount/2))) 
                    amtText[1-now] = "$%s" % (group(int(amount)))
            else:
                amtText0 = "0 %s" % (commodity)
                if amount<1:
                    amtText[now] = "%1.2f %s" % (float(amount/2), commodity) 
                    amtText[1-now] = "%1.2f %s" % (float(amount), commodity) 
                elif amount<10:
                    amtText[now] = "%1.1f %s" % (float(amount/2), commodity) 
                    amtText[1-now] = "%1.1f %s" % (float(amount), commodity) 
                else:
                    amtText[now] = "%s %s" % (group(int(amount/2)), commodity) 
                    amtText[1-now] = "%s %s" % (group(int(amount)), commodity)
            if explicit0==0:
                screenText[now] = "%s" % (amtText[now])
                screenText[1-now] = "%s" % (amtText[1-now])
                if probability==1:
                    screenText2[now] = "for sure"
                    screenText2[1-now] = "with a %s chance" % (delay)
                elif past==1:
                    screenText2[now] = "1 hour ago"
                    screenText2[1-now] = "%s ago" % (delay)
                else:
                    screenText2[now] = "now"
                    screenText2[1-now] = "in %s" % (delay)
            else:
                if probability==1:
                    screenText[now] = "%s for sure" % (amtText[now])
                    screenText2[now] = "%s with a %s chance" % (amtText0, delay)
                    screenText[1-now] = "%s for sure" % (amtText0)
                    screenText2[1-now] = "%s with a %s chance" % (amtText[1-now], delay)
                elif past==1:
                    screenText[now] = "%s 1 hour ago" % (amtText[now])
                    screenText2[now] = "%s %s ago" % (amtText0, delay)
                    screenText[1-now] = "%s 1 hour ago" % (amtText0)
                    screenText2[1-now] = "%s %s ago" % (amtText[1-now], delay)
                else:
                    screenText[now] = "%s now" % (amtText[now])
                    screenText2[now] = "%s in %s" % (amtText0, delay)
                    screenText[1-now] = "%s now" % (amtText0)
                    screenText2[1-now] = "%s in %s" % (amtText[1-now], delay)
            if losses==1:
                screenText[now] = "lose " + screenText[now]
                screenText[1-now] = "lose " + screenText[1-now]
                if explicit0==1:
                    screenText2[now] = "lose " + screenText2[now]
                    screenText2[1-now] = "lose " + screenText2[1-now]
            else:
                screenText[now] = "gain " + screenText[now]
                screenText[1-now] = "gain " + screenText[1-now]
                if explicit0==1:
                    screenText2[now] = "gain " + screenText2[now]
                    screenText2[1-now] = "gain " + screenText2[1-now]
            if (social==1) or (social==2):
                screenText2[now] = screenText2[now] + " for you alone"
                if explicit0==1:
                    screenText[now] = screenText[now] + " for you alone"
            if (social==1) or (social==3):
                screenText2[1-now] = screenText2[1-now] + " for you alone"
                if explicit0==1:
                    screenText[1-now] = screenText[1-now] + " for you alone"
            if (social==3) or (social==4):
                screenText2[now] = screenText2[now] + " for the group"
                if explicit0==1:
                    screenText[now] = screenText[now] + " for the group"
            if (social==2) or (social==4):
                screenText2[1-now] = screenText2[1-now] + " for the group"
                if explicit0==1:
                    screenText[1-now] = screenText[1-now] + " for the group"
            if explicit0==1:
                screenText[now] = screenText[now] + " and"
                screenText[1-now] = screenText[1-now] + " and"
            if gn_keystroke > 0:
                firsttime=1
                fixon = 1
                if (gn_keystroke == 1) & (now == 0):
                    response=1
                elif (gn_keystroke == 3) & (now == 1):
                    response=1
                else:
                    response=0
                isi=t
                isi_index=isi_index+1
                screenText[0] = ""
                screenText[1] = ""
                screenText2[0] = ""
                screenText2[1] = ""
                if question<4:
                    if losses==1:
                        qIndex = qIndex*2 if response==1 else (qIndex*2)-1
                    else:
                        qIndex = qIndex*2 if response==0 else (qIndex*2)-1
                else:
                    k = firstFive[question][qIndex-1][3] if response==1 else firstFive[question][qIndex-1][4]
                    ed50 = firstFive[question][qIndex-1][5] if response==1 else firstFive[question][qIndex-1][6]
                    gn_keystroke = 0
                logfile.write("%i,%f,%f,%s,%s,%i,%i\n" % (question, stim_onset, t, amount, delay, response, now))
                question = question+1
            
        #### End
        if question == 5:
            if probability==1:
                logfile.write("\nh,EP50\n")
            else:
                logfile.write("\nk,ED50\n")
            logfile.write("%s,%s\n" % (k, ed50))
            taskendon=1
            p.parameters.go_duration = (0, 'frames')  
                
    else:
        firsttime=1

    gn_keystroke = 0
    return 1 

def replaceLeftText(t):
    global screenText
    return screenText[0]

def replaceRightText(t):
    global screenText
    return screenText[1]
    
def replaceLeftText2(t):
    global screenText2
    return screenText2[0]

def replaceRightText2(t):
    global screenText2
    return screenText2[1]

def controlFix(t):
    global fixon
    if fixon:
        return 1
    else:
        return 0

def showNewSet(t):
    global newseton
    if newseton == 1:
        return 1
    else:
        return 0

def showTaskEnd(t):
    global taskendon
    if taskendon == 1:
        return 1
    else:
        return 0

def hideStim():  # only used before p starts
    return 0

def keydown(event):
        global gn_keystroke
        if event.key == pygame.locals.K_1:
                                        gn_keystroke = 1
        if event.key == pygame.locals.K_6:
                                        gn_keystroke = 3
        if event.key == pygame.locals.K_LEFT:
                                        gn_keystroke = 1
        if event.key == pygame.locals.K_RIGHT:
                                        gn_keystroke = 3
        if event.key == pygame.locals.K_ESCAPE:
                                        p.parameters.go_duration = (0, 'frames')
                                        # Quit presentation 'p' with esc press
                                   
def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + ','.join(reversed(groups))
    
### CONTROLLERS

trigger_in_controller = KeyboardTriggerInController(pygame.locals.K_5)
stimulus_on_controller = ConstantController(during_go_value=1,between_go_value=0)
stimulus_off_controller = ConstantController(during_go_value=0,between_go_value=1)
left_choice_controller = FunctionController(during_go_func=replaceLeftText)
right_choice_controller = FunctionController(during_go_func=replaceRightText)
left_choice2_controller = FunctionController(during_go_func=replaceLeftText2)
right_choice2_controller = FunctionController(during_go_func=replaceRightText2)
state_controller = FunctionController(during_go_func=getState)
fixation_controller = FunctionController(during_go_func=controlFix, between_go_func=hideStim)
newset_controller = FunctionController(during_go_func=showNewSet, between_go_func=hideStim)
taskend_controller = FunctionController(during_go_func=showTaskEnd, between_go_func=hideStim)

p.add_controller(p,'trigger_go_if_armed',trigger_in_controller)
p.add_controller(title,'on', stimulus_off_controller)
p.add_controller(title2,'on', stimulus_off_controller)
p.add_controller(left_choice,'on',stimulus_on_controller)
p.add_controller(right_choice,'on',stimulus_on_controller)
p.add_controller(left_choice2,'on',stimulus_on_controller)
p.add_controller(right_choice2,'on',stimulus_on_controller)
p.add_controller(left_choice,'text',left_choice_controller)
p.add_controller(left_choice2,'text',left_choice2_controller)
p.add_controller(right_choice,'text',right_choice_controller)
p.add_controller(right_choice2,'text',right_choice2_controller)
p.add_controller(fixation,'on',fixation_controller)
p.add_controller(newset,'on',newset_controller)
p.add_controller(taskend,'on',taskend_controller)
p.add_controller(p, 'trigger_go_if_armed', state_controller)

p.parameters.handle_event_callbacks = [(pygame.locals.KEYDOWN, keydown)]

p.go()
logfile.close()
