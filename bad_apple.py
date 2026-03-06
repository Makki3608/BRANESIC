import cv2
import numpy as np
import time

path = "../../Downloads/bad-apple.mp4"

cap = cv2.VideoCapture(path)
path = "badapple.bnf"
targetResolution = (14, 8)



open(path, "w").write("")



def WriteOutput():
    global branefuckLines
    open(path, "a").write(branefuckLines)
    branefuckLines = ""

lastChange = (0, 0, 0)
pointingAt = (0, 0, 1)
def GetCostToMove(currentC, targetC):
    cost = 1

    if currentC[0] != targetC[0]: cost += 4
    
    if currentC[1] != targetC[1]: cost += 2

    if currentC[2] != targetC[2]: cost += 5
    
    return cost


def SortChanges(changes):
    global lastChange
    sortedChanges = []
    while changes:
        cost = 0
        chosen = 0
        for l in range(len(changes)):
            candidateCost = GetCostToMove(lastChange, changes[l])
            if candidateCost < cost:
                cost = candidateCost
                chosen = l
        chosenChange = changes.pop(chosen)
        sortedChanges.append(chosenChange)
        lastChange = chosenChange
    return sortedChanges

branefuckSuffix = ""

moves = []
def DrawDifference(oldFrame, newFrame):
    global branefuckSuffix
    global branefuckLines
    global moves
    global pointingAt

    movesBuilding = ""
    whereDelta = np.bitwise_xor(oldFrame, newFrame)

    deltaLocations = np.column_stack(np.where(whereDelta == 255))

    

    changes = []
    for l in deltaLocations:
        changes.append((int(l[0]),int(l[1]),
        int(newFrame[l[0]][l[1]] / 255)))
    changes = SortChanges(changes)
    print(changes)

    if foo == showFrame:
        cv2.imshow("old", oldFrame)
        cv2.imshow("new", newFrame)
        cv2.imshow(str(changes), whereDelta)
    #if foo == 46: time.sleep(999999)
    #print(f"frame {foo}, {deltaLocations}")
    
    #print(whereDelta.shape)

    #cv2.imshow("difference", whereDelta)

    branefuckLines += "-["

    movesBuilding += ".]"
    movesBuilding += ">>>"

    for l in changes:
        movesBuilding += MoveBranefuck(l)
        movesBuilding += "#set_tile#"
    pointingAt = (0, 0, 1)

    moves.append(movesBuilding)

def MoveBranefuck(change):
    global pointingAt
    branefuckBuilding = ""

    differences = (change[0]-pointingAt[0], change[1]-pointingAt[1], change[2]-pointingAt[2])
    print(differences)

    if   differences[1] < 0: branefuckBuilding += str(differences[1])
    elif differences[1] > 0: branefuckBuilding += "+"+str(differences[1])

    if   differences[0] != 0: branefuckBuilding += "<" 
    if   differences[0] < 0: branefuckBuilding += str(differences[0])
    elif differences[0] > 0: branefuckBuilding += "+"+str(differences[0])

    if differences[2] != 0:
        branefuckBuilding += "<"
        if differences[0] == 0: branefuckBuilding += "<" 
        if   differences[2] ==   1: branefuckBuilding += "-6"
        elif differences[2] ==  -1: branefuckBuilding += "+6"

    if   differences[2] != 0: branefuckBuilding += ">>"
    elif differences[0] != 0: branefuckBuilding += ">"

    pointingAt = change
    return branefuckBuilding


previousFrame = np.zeros((8, 14), dtype=np.uint8)
def ProcessFrame(frame):
    global previousFrame
    global branefuckLines
    convertedFrame = cv2.resize(frame, targetResolution)
    convertedFrame[convertedFrame != 0] = 255

    DrawDifference(previousFrame, convertedFrame)

    previousFrame = convertedFrame
    WriteOutput()
    
    return convertedFrame

if not cap.isOpened():
    print("Cannot open camera")
    exit()

outputFile = open(path, 'a')

foo = 1
cutoff = 1800 #A
dumbPause = -1
showFrame = -48
startFrame = 1201
branefuckInitial =">+>,g:level_time,#mod#>[.]<#div#>>+<"
branefuckLines = "" + branefuckInitial
moves = []
branefuckSuffix = ""
if startFrame > 0:
    branefuckLines += f"-{startFrame-1}"

while True:
    ret, frame = cap.read()
    if not ret:break
    foo += 1
    if foo >= startFrame:
        WriteOutput()

        frame = frame[:, :, 0]
        processedFrame = ProcessFrame(frame)
        cv2.imshow('frame', processedFrame)
        if foo == showFrame: cv2.imshow('frame', processedFrame)
        #print(processedFrame.shape)
        if cv2.waitKey(1) == ord('q'):
            break

        #if foo == 20:
        #    time.sleep(20)
        if foo == cutoff: break
        if foo == dumbPause: time.sleep(999999)

print(f"number of frames: {foo-startFrame+1}")
outputFile.write(",t:0,-999.")
moves.reverse()
outputFile.write("".join(moves))
outputFile.write(branefuckSuffix)
cap.release() 

