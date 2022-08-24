import sys
import time
import numpy as np

#Set max printer speed
def setup(ser,max_XSpeed,max_ZSpeed):
    # Send Printer to home location
    time.sleep(2)
    ser.write(b'G28 W\r\n') #W is required to skip calibration
    checkOk(ser)

    #Tell 3D printer to use absolute coordinates
    ser.write(b'G90\n')
    checkOk(ser)

    ser.write(bytes('M203 X'+str(max_XSpeed)+' \n','utf-8')) #Set max X speed in mm/sec
    ser.write(bytes('M203 Z'+str(max_ZSpeed)+' \n','utf-8')) #Set max Z speed in mm/sec


#Ensures the printer sends an okay before moving to next command
def checkOk(ser):
    count = 0
    while True:
        a=ser.readline().decode('UTF-8')
        count+=1
        if a=="ok\n":
            return (1)
        if count > 50:
            sys.exit("Port Read Timed Out")

def genPoints(xStart,zStart,xSteps,zSteps,xSpace,zSpace,shape="L"):
    xCoord = np.array((np.arange(0,(xSteps),1)*xSpace)+ xStart)
    zCoord = np.array((np.arange(0,(zSteps),1)*zSpace)+ zStart)
    
    #Creates a square shaped measurement grid
    if shape == "square":
        measLocs = np.zeros((xSteps*zSteps,3))
        for iz,z in enumerate(zCoord):
            for ix,x in enumerate(xCoord):
                measLocs[iz*xSteps+ix,0] = x
                measLocs[iz*xSteps+ix,2] = z
                
    elif shape =="L":
        measLocs = np.zeros((xSteps+zSteps-1,3))
        #Sweep across X first
        for iX in np.arange(0,xSteps):
            measLocs[iX,0]=xCoord[iX]
            measLocs[iX,2]=zCoord[0]
        #Then sweep across Z
        for iZ in np.arange(0,zSteps-1):
            measLocs[xSteps+iZ,0] = xCoord[-1]
            measLocs[xSteps+iZ,2] = zCoord[iZ]
    return(measLocs)

#Tells the printer to move
def doMove(ser,coords,xSpeed,zSpeed):
    moveComX = 'G1'+ ' X'+str(coords[0])+' E0'+' F'+str(60*xSpeed)+' \r\n'
    ser.write(bytes(moveComX, 'utf-8'))
    isDone(ser)
    moveComZ = 'G1'+ ' Z'+str(coords[2])+' E0'+' F'+str(60*xSpeed)+' \r\n'
    ser.write(bytes(moveComZ, 'utf-8'))
    isDone(ser)

#First it checks that the move command responds with ok. Next
def isDone(ser):
    checkOk(ser)
    ser.write(b'M400\n') #Tells the printer to wait to finish the move before doing next task
    checkOk(ser)
    return(0)

#Save Current Time to files

