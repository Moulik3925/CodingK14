import random
import math
import numpy as np
import time

name = "V3_Moulik"
# 20 char team signal syntax
# 0,1 coordinates of island 1
# 2,3 coordinates of island 2
# 4,5 coordinates of island 3
# 6 curren State of the game X explore
# chr('65')='A'
# ord('A')=65
# 7 = oppCount


def replaceChar(string, posn, char):
    return (string[:posn]+char+string[posn+1:])

def islandGetInfo(island, sig):
    a = island*2 - 2
    x = ord(sig[a])
    y = ord(sig[a+1])
    return (x, y)

def updateIslandInfo(island, x, y, sig):
    a = island*2 - 2
    sig = sig[:a]+chr(x)+chr(y) + sig[a+2:]
    return sig
def moveTo(x, y, Pirate):
    position = Pirate.getPosition()
    if position[0] == x and position[1] == y:
        return 0
    if position[0] == x:
        return (position[1] < y) * 2 + 1
    if position[1] == y:
        return (position[0] > x) * 2 + 2
    if random.randint(1, 2) == 1:
        return (position[0] > x) * 2 + 2
    else:
        return (position[1] < y) * 2 + 1
def moveToSexy(x, y, Pirate, type):
    # using camel case (not my idea, I am not that lame)
    position = Pirate.getPosition()
    if type == "xFirst":
        if position[0] != x:
            return (position[0] > x) * 2 + 2
        else:
            return (position[1] < y) * 2 + 1
    elif type == "yFirst":
        if position[1] != y:
            return (position[1] < y) * 2 + 1
        else:
            return (position[0] > x) * 2 + 2
    elif type == "random":
        if random.randint(1, 2) == 1:
            return (position[0] > x) * 2 + 2
        else:
            return (position[1] < y) * 2 + 1

def inspectForIsland(pirate):
    data = np.array([[pirate.investigate_nw()[0], pirate.investigate_up()[0], pirate.investigate_ne()[0]], [pirate.investigate_left()[0], pirate.investigate_current()[0], pirate.investigate_right()[0]], [pirate.investigate_sw()[0], pirate.investigate_down()[0], pirate.investigate_se()[0]]])
    x, y = pirate.getPosition()
    # pirate.setSignal("")
    teamsig = pirate.trackPlayers()
    sig = pirate.getTeamSignal()
    for island in range(1, 4):
        if (sig[2*island-2] == chr(255)):
            a = (data == ("island"+str(island)))
            if (a[2][2] and not a[2][1] and not a[1][2]):
                sig = updateIslandInfo(island, x+2, y+2, sig)
            elif (a[2][2] and a[2][1] and not a[2][0]):
                sig = updateIslandInfo(island, x+1, y+2, sig)
            elif (a[2][2] and a[2][1] and a[2][0]):
                sig = updateIslandInfo(island, x, y+2, sig)
            elif (not a[2][2] and a[2][1] and a[2][0]):
                sig = updateIslandInfo(island, x-1, y+2, sig)
            elif (a[2][0] and not a[2][1] and not a[1][0]):
                sig = updateIslandInfo(island, x-2, y+2, sig)
            elif (a[2][0] and a[1][0] and not a[0][0]):
                sig = updateIslandInfo(island, x-2, y+1, sig)
            elif (a[2][0] and a[1][0] and a[0][0]):
                sig = updateIslandInfo(island, x-2, y, sig)
            elif (not a[2][0] and a[1][0] and a[0][0]):
                sig = updateIslandInfo(island, x-2, y-1, sig)
            elif (a[0][0] and not a[0][1] and not a[1][0]):
                sig = updateIslandInfo(island, x-2, y-2, sig)
            elif (a[0][0] and a[0][1] and not a[0][2]):
                sig = updateIslandInfo(island, x-1, y-2, sig)
            elif (a[0][0] and a[0][1] and a[0][2]):
                sig = updateIslandInfo(island, x, y-2, sig)
            elif (not a[0][0] and a[0][1] and a[0][2]):
                sig = updateIslandInfo(island, x+1, y-2, sig)
            elif (a[0][2] and not a[1][2] and not a[0][1]):
                sig = updateIslandInfo(island, x+2, y-2, sig)
            elif (a[0][2] and a[1][2] and not a[2][2]):
                sig = updateIslandInfo(island, x+2, y-1, sig)
            elif (a[0][2] and a[1][2] and a[2][2]):
                sig = updateIslandInfo(island, x+2, y, sig)
            elif (not a[0][2] and a[1][2] and a[2][2]):
                sig = updateIslandInfo(island, x+2, y+1, sig)
    pirate.setTeamSignal(sig)

def CaptureIslands(pirate,piratesig):
    status = pirate.trackPlayers()
    sig = pirate.getTeamSignal()
    selfsig = piratesig
    if (selfsig[3] == 'A'):
        island = 1
    elif (selfsig[3] == 'B'):
        island = 2
    elif (selfsig[3] == 'C'):
        island=3
    r = random.randint(1, 4)
    if(status[0]=='myCaptured' and status[1]=='myCaptured' and status[2]=='myCaptured'):
        return selfsig,0
    elif (island==1):
        if( ord(sig[0]) != 255 and (status[0] != 'myCaptured')):
            x = ord(sig[0])
            y = ord(sig[1])
            if r == 1:
                x += 1
                y += 1
            if r == 2:
                x += 1
                y -= 1
            if r == 3:
                x -= 1
                y -= 1
            if r == 4:
                x -= 1
                y += 1
            return selfsig,moveTo(x, y, pirate)
        else:
            # selfsig=replaceChar(selfsig,3,'B')
            selfsig=replaceChar(selfsig,3,'B''' if random.randint(1,2)==1 else 'C''')
    elif (island==2):
        if( ord(sig[2]) != 255 and (status[1] != 'myCaptured')):
            x = ord(sig[2])
            y = ord(sig[3])
            if r == 1:
                x += 1
                y += 1
            if r == 2:
                x += 1
                y -= 1
            if r == 3:
                x -= 1
                y -= 1
            if r == 4:
                x -= 1
                y += 1
            return selfsig,moveTo(x, y, pirate)
        else:
            selfsig=replaceChar(selfsig,3,'A' if random.randint(1,2)==1 else 'C')
            
            
    else:
        if( ord(sig[4]) != 255 and (status[2] != 'myCaptured')):
            x = ord(sig[4])
            y = ord(sig[5])
            if r == 1:
                x += 1
                y += 1
            if r == 2:
                x += 1
                y -= 1
            if r == 3:
                x -= 1
                y -= 1
            if r == 4:
                x -= 1
                y += 1
            return selfsig,moveTo(x, y, pirate)
        else:
            selfsig=replaceChar(selfsig,3,'A' if random.randint(1,2)==1 else 'B')
    pirate.setSignal(selfsig)
    return CaptureIslands(pirate,selfsig)

def isSpawned(pirate):
    # camel case, again, not my idea!!
    position = pirate.getPosition()
    base = pirate.getDeployPoint()
    if position[0] == base[0] and position[1] == base[1]:
        return True


def spawned(pirate):
    position = pirate.getPosition()
    base = pirate.getDeployPoint()
    if position[0] == base[0] and position[1] == base[1]:
        return (moveTo(pirate.getID() % 40, 0, pirate))


def ActPirate(pirate):
    rum = pirate.getTotalRum()
    wood = pirate.getTotalWood()
    gunpowder = pirate.getTotalGunpowder()
    l = pirate.trackPlayers()
    width = pirate.getDimensionX()
    height = pirate.getDimensionY()
    frame = pirate.getCurrentFrame()
    teamsig = str(pirate.getTeamSignal())
    deploy = pirate.getDeployPoint()
    selfsig = pirate.getSignal()
    status = pirate.trackPlayers()
    # initialising signals
    # 0 = id 1 = x, 2 = Y
    if (selfsig == ""):
        for i in range(20):
            selfsig += chr(255)
        selfsig = replaceChar(selfsig, 0, chr(int(pirate.getID())))
    posn = pirate.getPosition()
    id = int(pirate.getID()) % width
    inspectForIsland(pirate)
    if teamsig[6] == 'X' and selfsig[3] != 'C' and selfsig[3] != 'B' and selfsig[3] != 'A' and selfsig[3] != 'Y':
        selfsig = replaceChar(selfsig, 3, 'X')
    elif teamsig[6] == 'C':
        r = random.randint(1, 100)
        if r <= 30 and gunpowder <= 20 * ord(teamsig[6]):
            selfsig = replaceChar(selfsig, 3, 'G')
            x = random.randint(0, width-1)
            y = random.randint(0, width-1)
            selfsig = replaceChar(selfsig, 4, chr(x))
            selfsig = replaceChar(selfsig, 5, chr(y))
        elif(selfsig[3]!='A' and selfsig[3]!='B' and selfsig[3]!='C' and selfsig[3]!='G'):
            p = random.randint(1,3)
            if(r==1 and status[0]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'A')
            elif(r==2 and status[1]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'B')
            elif(r==3 and status[2]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'C')
    elif teamsig[6] == 'G':
        if (gunpowder >= 50 * ord(selfsig[10])):
            teamsig = replaceChar(teamsig, 6, 'C')
            pirate.setTeamSignal(teamsig)
    if (selfsig[3]=='Y'):
        if (posn[1] == (height-1 if not (deploy[1] == 0) else 0)):
            r=random.randint(1,3)
            if(r==1 and status[0]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'A')
            elif(r==2 and status[1]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'B')
            elif (r==3 and status[2]!='myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'C')
        if (posn[0] == (width-id if deploy[0] == 0 else id-1)):
            finalReturn = moveTo(
                posn[0], height-1 if not(deploy[1] == 0) else 0, pirate)
        else:
            finalReturn = moveToSexy((width-id if deploy[0] == 0 else id), (id - 1 if deploy[1] == 0 else deploy[1]+1-id), pirate, "yFirst")
    if (selfsig[3] == 'X'):
        # pirate signal change to C if the pirate has landed where it was intended to
        if (posn[1] == (height-1 if deploy[1] == 0 else 0)):
            selfsig = replaceChar(selfsig, 3, 'Y')
        if (posn[0] == (width-id if deploy[0] == 0 else id-1)):
            finalReturn = moveTo(
                posn[0], height-1 if deploy[1] == 0 else 0, pirate)
        else:
            finalReturn = moveToSexy((width-id if deploy[0] == 0 else (id-1) % width), ((
                deploy[1]+id - 1) % width if deploy[1] == 0 else deploy[1]+1-id), pirate, "yFirst")
    elif(selfsig[3] == 'A' or selfsig[3] == 'B' or selfsig[3] == 'C'):
        selfsig, finalReturn= CaptureIslands(pirate,selfsig)
    elif selfsig[3] == 'G':
        # if selfsig[3] != 'G'\
        x = ord(selfsig[4])
        y = ord(selfsig[5])
        if (posn[0] == x and posn[1] == y):
            x = random.randint(0, width-1)
            x = (int(pirate.getID()) + x)%width
            y = width - 1 - y
            selfsig = replaceChar(selfsig, 4, chr(x))
            selfsig = replaceChar(selfsig, 5, chr(y))
            pirate.setSignal(selfsig)
        op = random.randint(1 , 2)
        if op == 1:
            finalReturn = moveToSexy(x, y, pirate, "xFirst")
        else:
            finalReturn = moveToSexy(x , y , pirate , "yFirst")
    # updating X and Y positions
    if (finalReturn == 1):
        selfsig = replaceChar(selfsig, 2, chr(max(0, posn[1]-1)))
    elif (finalReturn == 3):
        selfsig = replaceChar(selfsig, 2, chr(min(height, (posn[1]+1))))
    elif (finalReturn == 2):
        selfsig = replaceChar(selfsig, 1, chr((min(width, posn[0]+1))))
    elif (finalReturn == 4):
        selfsig = replaceChar(selfsig, 1, chr(max(0, posn[0]-1)))
    pirate.setSignal(selfsig)
    return finalReturn


def ActTeam(team):
    pirateNumber = team.getTotalPirates()
    rum = team.getTotalRum()
    wood = team.getTotalWood()
    gunpowder = team.getTotalGunpowder()
    signals = team.getListOfSignals()
    l = team.trackPlayers()
    teamsig = team.getTeamSignal()
    width = team.getDimensionX()
    height = team.getDimensionY()
    frame = team.getCurrentFrame()
    status = team.trackPlayers()
    if teamsig == "":
        for i in range(20):
            teamsig += chr(255)
        teamsig = replaceChar(teamsig, 6, 'X')
        teamsig = replaceChar(teamsig, 7, chr(8))
    if frame >= 178:
        teamsig = replaceChar(teamsig, 6, 'C')
    team.setTeamSignal(teamsig)

    # for gettin max number of living opponents
    initialPirates = 16  # 8+8 of team blue and team red
    totalRum = (width*height*1.5)//16  # in terms of pirates
    currentAlive = len(signals)
    i = 0
    maxAlive = 8
    while (i+1 < len(signals) and signals[i+1] != ""):
        maxAlive = ord(signals[i][0]) + len(signals) - i
        i += 1
    killed = maxAlive - currentAlive
    maxOpp = totalRum + initialPirates - killed
    # Count of Maximum Opponents
    if(maxOpp >= 255):
        maxOpp = 255
    teamsig = replaceChar(teamsig,10,chr(int(maxOpp)))

    # setTeamsig = G if any pirate has G
    for signal in signals:
        if (signal != ""):
            if signal[3] == 'G':
                teamsig = replaceChar(teamsig, 6, 'G')
                team.setTeamSignal(teamsig)
                break
    Y = 0
    G = 0 
    A = 0
    B = 0
    C = 0
    for signal in signals:
        if (signal!= ""):
            if signal[3]=='G':G+=1
            if signal[3] == 'Y': Y+=1
            elif signal[3] == 'A': A+=1
            elif signal[3] == 'B': B+=1
            elif signal[3] == 'C': C+=1
    print(Y,G,A,B,C) 

    # team.buildWalls(1)
    # team.buildWalls(2)
    # team.buildWalls(3)
    # if  teamsig:
    #     island_no = int (teamsig[0])
    #     signal = l[island_no - 1]
    #     if signal == "myCaptured":
    #         team.setTeamSignal("")
