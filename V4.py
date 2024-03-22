import random
import math
import numpy as np
import time

name = "V4"
# 20 char team signal syntax
# 0,1 coordinates of island 1
# 2,3 coordinates of island 2
# 4,5 coordinates of island 3
# 6 curren State of the game X explore
# chr('65')='A'
# ord('A')=65
# 7 = oppCount


def debugSignal(signal):
    for char in signal:
        print(ord(char), end=',')
    print()


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
    data = np.array([[pirate.investigate_nw()[0], pirate.investigate_up()[0], pirate.investigate_ne()[0]], [pirate.investigate_left()[
                    0], pirate.investigate_current()[0], pirate.investigate_right()[0]], [pirate.investigate_sw()[0], pirate.investigate_down()[0], pirate.investigate_se()[0]]])
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


def CaptureIslands(pirate, piratesig):
    status = pirate.trackPlayers()
    sig = pirate.getTeamSignal()
    selfsig = piratesig
    if (selfsig[3] == 'A'):
        island = 1
    elif (selfsig[3] == 'B'):
        island = 2
    elif (selfsig[3] == 'C'):
        island = 3
    r = random.randint(1, 4)
    if (status[0] == 'myCaptured' and status[1] == 'myCaptured' and status[2] == 'myCaptured'):
        return selfsig, 0
    elif (island == 1):
        if (ord(sig[0]) != 255 and (status[0] != 'myCaptured')):
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
            return selfsig, moveTo(x, y, pirate)
        else:
            # selfsig=replaceChar(selfsig,3,'B')
            selfsig = replaceChar(
                selfsig, 3, 'B''' if random.randint(1, 2) == 1 else 'C''')
    elif (island == 2):
        if (ord(sig[2]) != 255 and (status[1] != 'myCaptured')):
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
            return selfsig, moveTo(x, y, pirate)
        else:
            selfsig = replaceChar(
                selfsig, 3, 'A' if random.randint(1, 2) == 1 else 'C')

    else:
        if (ord(sig[4]) != 255 and (status[2] != 'myCaptured')):
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
            return selfsig, moveTo(x, y, pirate)
        else:
            selfsig = replaceChar(
                selfsig, 3, 'A' if random.randint(1, 2) == 1 else 'B')
    # debugSignal(selfsig)
    pirate.setSignal(selfsig)
    return CaptureIslands(pirate, selfsig)


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


def enemyPresent(pirate):
    posn = pirate.getPosition()
    # chutiya moulik and abhi forcedme to change the name of the variable!!
    teamSig = str(pirate.getTeamSignal())
    if (abs(posn[0] - ord(teamSig[0])) <= 1 and abs(posn[1] - ord(teamSig[1])) <= 1) or (abs(posn[0] - ord(teamSig[2])) <= 1 and abs(posn[1] - ord(teamSig[3])) <= 1) or (abs(posn[0] - ord(teamSig[4])) <= 1 and abs(posn[1] - ord(teamSig[5])) <= 1):
        data = np.array([[pirate.investigate_nw()[1], pirate.investigate_up()[1], pirate.investigate_ne()[1]], [pirate.investigate_left()[
                        1], pirate.investigate_current()[1], pirate.investigate_right()[1]], [pirate.investigate_sw()[1], pirate.investigate_down()[1], pirate.investigate_se()[1]]])
        data = (data == "enemy")
        # print(data)
        for who in data:
            if who.any() == True:
                return True
    return False


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
    elif teamsig[6] == 'C' or teamsig[6] == 'F':
        r = random.randint(1, 100)
        if teamsig[6]=='C' and r <= 50 and gunpowder <= 15 * ord(teamsig[6]):
            selfsig = replaceChar(selfsig, 3, 'G')
            y = random.randint(0, 1)
            if y == 1:
                y = height-1
            x = (int(pirate.getID()) + r) % width
            selfsig = replaceChar(selfsig, 4, chr(x))
            selfsig = replaceChar(selfsig, 5, chr(y))
        elif (selfsig[3] != 'A' and selfsig[3] != 'B' and selfsig[3] != 'C' and selfsig[3] != 'G'):
            p = random.randint(1, 3)
            if (r == 1 and status[0] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'A')
            elif (r == 2 and status[1] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'B')
            elif (r == 3 and status[2] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'C')
    elif teamsig[6] == 'G':
        # print(ord(teamsig[11]),ord(teamsig[12]),ord(teamsig[13]),sep=",")
        if ((gunpowder >= 40 * ord(selfsig[10])) or (ord(teamsig[11]) == 0 and status[0]!='myCaptured') or (ord(teamsig[12]) == 0 and status[1]!='myCaptured') or (ord(teamsig[13]) == 0 and status[2]!='myCaptured')):
        # if (True):
            teamsig = replaceChar(teamsig, 6, 'F')
            pirate.setTeamSignal(teamsig)

    finalReturn = 0
    # SelfSignals
    if (selfsig[3] == 'Y'):
        if (posn[1] == (height-1 if not (deploy[1] == 0) else 0)):
            r = random.randint(1, 3)
            if (r == 1 and status[0] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'A')
            elif (r == 2 and status[1] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'B')
            elif (r == 3 and status[2] != 'myCaptured'):
                selfsig = replaceChar(selfsig, 3, 'C')
        if (posn[0] == (width-id if deploy[0] == 0 else id-1)):
            finalReturn = moveTo(
                posn[0], height-1 if not (deploy[1] == 0) else 0, pirate)
        else:
            finalReturn = moveToSexy(
                (width-id if deploy[0] == 0 else id), (id - 1 if deploy[1] == 0 else deploy[1]+1-id), pirate, "yFirst")
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
    elif (selfsig[3] == 'A' or selfsig[3] == 'B' or selfsig[3] == 'C'):
        selfsig, finalReturn = CaptureIslands(pirate, selfsig)
    elif selfsig[3] == 'G':
        x = ord(selfsig[4])
        y = ord(selfsig[5])
        if (posn[0] == x and posn[1] == y):
            x = random.randint(0, width-1)
            x = (int(pirate.getID()) + x) % width
            y = random.randint(0, 1)
            if y == 1:
                y = height-1
            selfsig = replaceChar(selfsig, 4, chr(x))
            selfsig = replaceChar(selfsig, 5, chr(y))
            pirate.setSignal(selfsig)
        op = random.randint(1, 2)
        if op == 1:
            finalReturn = moveToSexy(x, y, pirate, "xFirst")
        else:
            finalReturn = moveToSexy(x, y, pirate, "yFirst")
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
    teamsig = pirate.getTeamSignal()
    if enemyPresent(pirate):
        if selfsig[3] == 'A':
            # print("A")
            teamsig = replaceChar(teamsig, 7, 'Y')
        if selfsig[3] == 'B':
            # print("B")
            teamsig = replaceChar(teamsig, 8, 'Y')
        if selfsig[3] == 'C':
            # print("C")
            teamsig = replaceChar(teamsig, 9, 'Y')
    pirate.setTeamSignal(teamsig)
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
    if (maxOpp >= 255):
        maxOpp = 255
    teamsig = replaceChar(teamsig, 10, chr(int(maxOpp)))

    # setTeamsig = G if any pirate has G
    for signal in signals:
        if (signal != ""):
            if signal[3] == 'G':
                teamsig = replaceChar(teamsig, 6, 'G')
                team.setTeamSignal(teamsig)
                break
    if teamsig[7] == 'Y':
        team.buildWalls(1)
        teamsig = replaceChar(teamsig, 7, 'N')
    if teamsig[8] == 'Y':
        team.buildWalls(2)
        teamsig = replaceChar(teamsig, 8, 'N')
    if teamsig[9] == 'Y':
        team.buildWalls(3)
        teamsig = replaceChar(teamsig, 9, 'N')


    # if teamsig[6] =='X':
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
    teamsig=replaceChar(teamsig,11,chr(A))
    teamsig=replaceChar(teamsig,12,chr(B))
    teamsig=replaceChar(teamsig,13,chr(C))
    teamsig=replaceChar(teamsig,14,chr(G))
    teamsig=replaceChar(teamsig,15,chr(Y))
    team.setTeamSignal(teamsig)
    print(Y,G,A,B,C)

    # team.buildWalls(1)
    # team.buildWalls(2)
    # team.buildWalls(3)
    # if  teamsig:
    #     island_no = int (teamsig[0])
    #     signal = l[island_no - 1]
    #     if signal == "myCaptured":
    #         team.setTeamSignal("")

    # for char in teamsig:
