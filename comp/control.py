import pyautogui
import time

#Inits the printer and goes to first measurement point
pyautogui.click(x=1764,y=360,clicks=1,button='left')
pyautogui.typewrite('python printControl.py \n')

#Waits to complete initialization
time.sleep(25)

#Arms DCA mmWaveStudio
pyautogui.click(x=90,y=530,clicks=1,button='left')
time.sleep(1)
#Arms Triggers mmWaveStudio
pyautogui.click(x=212,y=530,clicks=1,button='left')
#Tells printer to start scanning
pyautogui.click(x=1764,y=360,clicks=1,button='left')
pyautogui.typewrite('yes\n')