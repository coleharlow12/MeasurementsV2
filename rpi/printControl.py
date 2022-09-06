import sys
import time
import serial
import pandas as pd
import numpy as np
import gpiozero
from signal import pause
from utils import (
                   checkOk,
                   genPoints,
                   setup,
                   doMove,
                   )
import pickle
import os
    
#Printer Setup
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

maxX = 35 #mm/s
maxZ = 35 #mm/s

setup(ser,maxX,maxZ)

# Generate the grid to stop at
mLocs = genPoints(xStart=30,zStart=30,xSteps=8,zSteps=16,xSpace=5,zSpace=2.5,shape="L")

# Create Pandas dataframe to store the data
cols = ['x coord','y coord','z coord','time']
df = pd.DataFrame(index=range(mLocs.shape[0]),columns=cols)

# Move to First Measurement Point
doMove(ser=ser,coords=mLocs[0,:],xSpeed=maxX,zSpeed=maxZ)
df.iloc[0,:] = [mLocs[0,0],mLocs[0,1],mLocs[0,2],(0)]

# Set variables for measurement
restTime = 8000*1e-6 #Time in us to wait

TRIGGERPIN = 3 #Used to trigger the mmWaveRadar

led = gpiozero.LED(TRIGGERPIN)
led.off

txt = input('Init Complete. Continue? ')
if txt=='yes':
    # Starts the measurements of the radar
    led.on    
    tstart = time.perf_counter()

    for coordIn in range(1,(mLocs.shape[0])):
        time.sleep(restTime)
        # Move to the First Measurement Location
        doMove(ser=ser,coords=mLocs[coordIn,:],xSpeed=maxX,zSpeed=maxZ)
        df.iloc[coordIn,:]=[mLocs[coordIn,0],mLocs[coordIn,1],mLocs[coordIn,2],
                            (time.perf_counter()-tstart)]
        
    print(df)
    cwd = os.getcwd()
    measNum = 1

    if os.path.isdir(os.path.join(cwd,'measTimeandLoc')):
        df.to_csv(os.path.join(cwd,'measTimeandLoc',("meas"+str(measNum))))
                  
    else:
        os.mkdir(os.path.join(cwd,'measTimeandLoc'))
        df.to_csv(os.path.join(cwd,'measTimeandLoc',("meas"+str(measNum))))
        
              


