#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        dinoActor.py
#
# Purpose:     This module is used to start chrome browswer and play the google 
#              dino game. We follow this example : 
#              https://www.geeksforgeeks.org/google-chrome-dino-bot-using-image-recognition-python/
# 
# Author:      Yuancheng Liu
#
# Version:     v_0.1
# Created:     2022/12/12
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os
import time
import threading
import numpy as np

import pyautogui
from PIL import ImageGrab, ImageOps

# change to use new webdriver-manager module : https://pypi.org/project/webdriver-manager/
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

GAME_URL = 'chrome://dino/'
REP_POS = (460, 421)        # screen coordinates of replay button to start the game. 
DINO_FR_POS = (190, 440)    # dinaso front rectangle box position on the screen.

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class dinoActor(object):

    def __init__(self, driverPath=None, playtime=0):
        """ init the dinasaur play actor.
        Args:
            driverPath (_type_, optional): The google driver(exe) path. Defaults to None.
            playtime (int, optional): how many second you want to play. Defaults to 0.
        """
        # dirpath = os.path.dirname(__file__)
        # chromeDriverPath = driverPath if driverPath else os.path.join(dirpath, 'chromedriver.exe')
        # self.driver = webdriver.Chrome(executable_path=chromeDriverPath)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.replaybutton = (REP_POS[0], REP_POS[1], REP_POS[0]+60, REP_POS[1]+50)
        self.dinasaurFbox = (DINO_FR_POS[0]+30, DINO_FR_POS[1], DINO_FR_POS[0]+120, DINO_FR_POS[1]+2)
        self.playtime = playtime    # set how long you want the actor play.
        self.timerTH = None         # timer to reset or terminate the play.
        self.startT = 0
        self.terminate = False
        self.resetParm = 0

#-----------------------------------------------------------------------------
    def restartGame(self):
        # using pyautogui library, we are clicking on the replay button without any user interaction
        pyautogui.click(self.replaybutton)
        # we will keep our Bot always down that will prevent him to get hit by bird
        pyautogui.press('space')
        #pyautogui.keyDown('space')
        #pyautogui.keyUp('space')
        #pyautogui.keyDown('down')

#-----------------------------------------------------------------------------
    def jump(self):
        # pyautogui.keyUp('down') # releasing the Down Key
        # pressing Space to overcome Bush
        pyautogui.keyDown('space')
        # so that Space Key will be recognized easily
        time.sleep(0.15)
        # releasing the Space Key
        pyautogui.keyUp('space')
        # again pressing the Down Key to keep my Bot always down
        #pyautogui.keyDown('down')

#-----------------------------------------------------------------------------
    def imageGrab(self, box):
        # defining the coordinates of box in front of dinosaur
        # grabbing all the pixels values in form of RGB tuples
        image = ImageGrab.grab(box)
        # converting RGB to Grayscale to make processing easy and result faster
        grayImage = ImageOps.grayscale(image)
        # using numpy to get sum of all grayscale pixels
        a = np.array(grayImage.getcolors())
        #print(a.sum())
        return a.sum() # returning the sum

#-----------------------------------------------------------------------------
    def timeCount(self):
        while True:
            crtTime = time.time()
            if self.playtime > 0 and crtTime - self.startT > self.playtime:
                self.terminate = True
                return
            time.sleep(5)
            # check whether need to reset.
            if self.resetParm > 0 and self.resetParm == self.imageGrab(self.replaybutton):
                self.restartGame()
            else:
                self.resetParm = self.imageGrab(self.replaybutton)

#-----------------------------------------------------------------------------
    def play(self):
        self.startT = time.time()
        try:
            self.driver.get(GAME_URL)
        except Exception as err:
            print('Ignore some internet not access exception %s' %str(err))
        time.sleep(3) # Wait chrome load the web.
        pyautogui.press('space')
        time.sleep(2)
        pyautogui.press('space') # Get start
        time.sleep(0.1)
        self.timerTH = threading.Timer(10.0, self.timeCount)  
        self.timerTH.start()
        self.restartGame()

        # Main loop to play the game.
        while not self.terminate:
            if(self.imageGrab(self.dinasaurFbox)!= 435):
                self.jump()
                # time to recognize the operation performed by above function
                time.sleep(0.05)
        
        if self.timerTH: self.timerTH.cancel()
        self.driver.quit()
        print("end!")

#-----------------------------------------------------------------------------
def testCase(mode=0):
    if mode == 1:
        actor = dinoActor(playtime=40)
        actor.play()
        print("Finish")
    else:
        pass  

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    testCase(mode=1)
