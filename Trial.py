import random
import math
import numpy as np

name = "CodingK14"
print(name)
# 20 char team signal syntax
# 0,1 coordinates of island 1
# 2,3 coordinates of island 2
# 4,5 coordinates of island 3
# 6 curren State of the game X explore
# chr('65')='A'
# ord('A')=65
def replaceChar(string,posn,char):
    return (string[:posn]+char+string[posn+1:])
def islandGetInfo(island, sig):
    a = island*2 - 2
    x = ord(sig[a])
    y = ord(sig[a+1])
    return (x, y)

def updateIslandInfo(island,x,y,sig):
    a = island*2 - 2
    sig = sig[:a]+chr(x)+chr(y) + sig[a+2:]
    # sig[a] = chr(x)
    # sig[a+1] = chr(y)
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

def moveToSexy(x , y , Pirate , type):
    #using camel case (not my idea, I am not that lame)
    position = Pirate.getPosition()
    if type == "xFirst" :
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
   
    # OXXXX
    # X...X
    # X...X 
    # X...X
    # XXXXX
    data = np.array([[pirate.investigate_nw()[0],pirate.investigate_up()[0],pirate.investigate_ne()[0]],[pirate.investigate_left()[0],pirate.investigate_current()[0],pirate.investigate_right()[0]],[pirate.investigate_se()[0],pirate.investigate_down()[0],pirate.investigate_se()[0]]])
    x, y = pirate.getPosition()
    pirate.setSignal("")
    teamsig = pirate.trackPlayers()
    sig = pirate.getTeamSignal()
    for island in range(1,4):
        if(sig[2*island-2]==chr(127)):
            a = (data==("island"+str(island)))
            # print(a)
            if(a[2][2] and not a[2][1] and not a[1][2]):
                sig=updateIslandInfo(island,x+2,y+2,sig)
            elif (a[2][2] and a[2][1] and not a[2][0]):
                sig=updateIslandInfo(island,x+1,y+2,sig)
            elif (a[2][2] and a[2][1] and a[2][0]):
                sig=updateIslandInfo(island,x,y+2,sig)
            elif (not a[2][2] and a[2][1] and a[2][0]):
                sig=updateIslandInfo(island,x-1,y+2,sig)
            elif (a[2][0] and not a[2][1] and not a[1][0]):
                sig=updateIslandInfo(island,x-2,y+2,sig)
            elif (a[2][0] and a[1][0] and not a[0][0]):
                sig=updateIslandInfo(island,x-2,y+1,sig)
            elif (a[2][0] and a[1][0] and a[0][0]):
                sig=updateIslandInfo(island,x-2,y,sig)
            elif (not a[2][0] and a[1][0] and a[0][0]):
                sig=updateIslandInfo(island,x-2,y-1,sig)
            elif (a[0][0] and not a[0][1] and not a[1][0]):
                sig=updateIslandInfo(island,x-2,y-2,sig)
            elif (a[0][0] and a[0][1] and not a[0][2]):
                sig=updateIslandInfo(island,x-1,y-2,sig)
            elif (a[0][0] and a[0][1] and a[0][2]):
                sig=updateIslandInfo(island,x,y-2,sig)
            elif (not a[0][0] and a[0][1] and a[0][2]):
                sig=updateIslandInfo(island,x+1,y-2,sig)
            elif (a[0][2] and not a[1][2] and not a[0][1]):
                sig=updateIslandInfo(island,x+2,y-2,sig)
            elif (a[0][2] and a[1][2] and not a[2][2]):
                sig=updateIslandInfo(island,x+2,y-1,sig)
            elif (a[0][2] and a[1][2] and a[2][2]):
                sig=updateIslandInfo(island,x+2,y,sig)
            elif (not a[0][2] and a[1][2] and a[2][2]):
                sig=updateIslandInfo(island,x+2,y+1,sig)
    pirate.setTeamSignal(sig)
# def sendAttackForce(x,y):
def CaptureIslands(pirate):
    status = pirate.trackPlayers()
    # print(status)
    sig = pirate.getTeamSignal()
    # print(type(sig[0]))
    r = random.randint(1,4)
    # print (status[0],status[1],status[2],sep=',')
    if (ord(sig[0])!='127'and (status[0]!='myCaptured')):
        x=ord(sig[0]) 
        y=ord(sig[1])
        if r==1:
            x+=1
            y+=1
        if r==2:
            x+=1
            y-=1
        if r==3:
            x-=1
            y-=1
        if r==4:
            x-=1
            y+=1
        return(moveTo(x,y,pirate))
    if (ord(sig[2])!='127'and (status[1]!='myCaptured')):
        x=ord(sig[2]) 
        y=ord(sig[3])
        if r==1:
            x+=1
            y+=1
        if r==2:
            x+=1
            y-=1
        if r==3:
            x-=1
            y-=1
        if r==4:
            x-=1
            y+=1
        return(moveTo(x,y,pirate))
    if (ord(sig[4])!='127'and (status[2]!='myCaptured')):
        x=ord(sig[4]) 
        y=ord(sig[5])
        if r==1:
            x+=1
            y+=1
        if r==2:
            x+=1
            y-=1
        if r==3:
            x-=1
            y-=1
        if r==4:
            x-=1
            y+=1
        return(moveTo(x,y,pirate))
def isSpawned(pirate):
    #camel case, again, not my idea!!
    position = pirate.getPosition()
    base = pirate.getDeployPoint()
    if position[0] == base[0] and position[1] == base[1]:
        return True

def spawned(pirate):
    position = pirate.getPosition()
    base = pirate.getDeployPoint()
    if position[0] == base[0] and position[1] == base[1]:
        return (moveTo(pirate.getID()%40 , 0 , pirate))
    
def lowGunPowder(pirate , n):
    moveToSexy((pirate.getID() + n)%40 , 0 , pirate , "xFirst")

#def zigzag(pirate):

    
def ActPirate(pirate):
    rum=pirate.getTotalRum()
    wood=pirate.getTotalWood()
    gunpowder=pirate.getTotalGunpowder()
    l = pirate.trackPlayers()
    width = pirate.getDimensionX()    
    height = pirate.getDimensionY()
    frame = pirate.getCurrentFrame()
    teamsig = str(pirate.getTeamSignal())
    deploy = pirate.getDeployPoint()
    selfsig = pirate.getSignal()
    posn = pirate.getPosition()
    # id = int(pirate.getID())
    id = int(pirate.getID())%width
    
    inspectForIsland(pirate)
    print(teamsig)
    if selfsig == "":
        for i in range(20):
            selfsig+=chr(127)
    if teamsig[6]=='X':
        selfsig=replaceChar(selfsig, 3,'X')
        print("X mode")
    elif teamsig[6]=='C':
        if (selfsig[3] != 'G' and selfsig[3]!='C'):
            r = random.randint(1,100)
            if r<=25 and gunpowder <= 1000:
                selfsig=replaceChar(selfsig, 3,'G')
                print("G mode")
            else:
                selfsig=replaceChar(selfsig, 3,'C')
                print("C mode")
                #selfsig=replaceChar(selfsig,3,'C') 
    # if (len(teamsig)>6 and teamsig[6]=='X'):
    if (selfsig[3]=='X'):
    # if True:
        # if (posn[0]==(width+1-id if deploy[0]==0 else id-1) and posn[1]==(deploy[1]+id -1 if deploy[1]==0 else deploy[1]+1-id)):
        if (posn[0]==(width-id if deploy[0]==0 else id-1)):
            # selfsig[3]='1'
            return moveTo(posn[0],height-1 if deploy[1]==0 else 0,pirate)
        else:
            return moveToSexy((width-id if deploy[0]==0 else (id-1)%width),((deploy[1]+id -1)%width if deploy[1]==0 else deploy[1]+1-id),pirate,"yFirst")
    if (selfsig[3]=='C'):
        return CaptureIslands(pirate)
    if selfsig[3] == 'G':
        # if selfsig[3] != 'G' 
        return lowGunPowder(pirate , r)
    if gunpowder >= 1500:
        selfsig = replaceChar(selfsig , 3 , 'C')

def ActTeam(team):
    pirateNumber=team.getTotalPirates()
    rum=team.getTotalRum()
    wood=team.getTotalWood()
    gunpowder=team.getTotalGunpowder()
    signals=team.getListOfSignals()
    l = team.trackPlayers()
    teamsig = team.getTeamSignal()
    width = team.getDimensionX()
    height = team.getDimensionY()
    frame = team.getCurrentFrame()
    status=team.trackPlayers()
    PirateList = team.getListOfSignals()
    # print(len(PirateList))
    # print (status)
    if teamsig == "":
        for i in range(20):
            teamsig+=chr(127)
        teamsig=replaceChar(teamsig,6,'X')
    if frame>=178:
        teamsig=replaceChar(teamsig,6,'C')
    if teamsig[6] != 'X' and team.getTotalGunpowder() <= 1000:
        teamsig=replaceChar(teamsig,6,'G')
    team.setTeamSignal(teamsig)
    # for char in teamsig[:6]:
    #     print (ord(char),end=" ")
    # print()
    

    # if teamsig[6] =='X':
        
    # team.buildWalls(1)
    # team.buildWalls(2)
    # team.buildWalls(3)
    # # print(team.getTeamSignal())
    # # print(team.trackPlayers())
    # if  teamsig:
    #     island_no = int (teamsig[0])
    #     signal = l[island_no - 1]
    #     if signal == "myCaptured":
    #         team.setTeamSignal("")
