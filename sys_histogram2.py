#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import multiprocessing
import time
import psutil
from datetime import datetime
<<<<<<< HEAD

=======
from numpy import interp, zeros
>>>>>>> ab6e6ebb2d764b9ccc9e57a8425adb7c20502009
from demo_opts import get_device
from luma.core.render import canvas
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008



# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Longer refresh rate the more history is shown
# If you set this to e.x. 30 sec you will get about 25 minutes of history on the graph
REFRESH_INTERVAL = 0.1

# FlipFlop blink variable
blnk = 1


def init_histogram():
    # HistogramSettings
    histogramResolution = 56
    histogramTime = []
    histogramData = []
    x = 100
    # Filling up the arrays for the histogram
    for pix in range(0, histogramResolution):
        x -= 2
        if x > 2:
            histogramTime.append(x)

    for timeLen in range(0, len(histogramTime)):
        histogramData.append(60)

    return histogramData, histogramTime

def mainhist(device):
    READ_ADC = mcp.read_adc(0)
    INDEX_VAL = int(interp(READ_ADC,[0,1023],[0,127]))
    minHistHeight = 63
    maxHistHeight = 0
    minHistLenght = 0
    maxHistLenght = 127
    HIST_VALUES[INDEX_VAL] += 1
      #LIST OF INDECES FOR DRAWING VERTICAL LINE FOR EACH CHANNEL
    
    with canvas(device, dither=True) as draw:
        draw.rectangle((minHistLenght, maxHistHeight, maxHistLenght, minHistHeight), outline="white")
        for i in range(minHistLenght,maxHistLenght):
            draw.line((minHistLenght+i,minHistHeight,minHistLenght+i,63-HIST_VALUES[i]), fill="orange")
    
    
    
def main(device, histogramData, histogramTime,peak):
    # Importing some global vars
    global blnk

    

    # Histogram graph
    READ_ADC = [0]
    READ_ADC[0] = 5 * mcp.read_adc(0)/1023 #os.getloadavg()
    #print(READ_ADC)
    
    cpuPercent = (READ_ADC[0]/4) * 100
    minHistHeight = 63
    maxHistHeight = 16
    minHistLenght = 3
    maxHistLenght = 124

    histogramHeight = (((100 - cpuPercent) * (minHistHeight - maxHistHeight)) / 100) + maxHistHeight
    
    # Starting the canvas for the screen
    with canvas(device, dither=True) as draw:


        # Histogram Outline
        draw.rectangle((minHistLenght, maxHistHeight, maxHistLenght, minHistHeight), outline="white")




        # last peak
        if peak[0]>peak[1]:
            
            draw.text((0, 0), "Last peak: " + "{0:.2f}".format(peak[0]), fill="white")
        else:
            
            draw.text((0, 0), "Last peak: " + "{0:.2f}".format(peak[1]), fill="white")

    
        # Histogram
        histogramData.insert(0, histogramHeight)
        for htime in range(0, len(histogramTime) - 1):
            timePlusOne = htime + 1
            if histogramData[0] > maxHistHeight:
                draw.line((histogramTime[timePlusOne], histogramData[timePlusOne], histogramTime[htime], histogramData[htime]), fill="orange")
            else:
                histogramData[0] = maxHistHeight
                draw.text(((minHistLenght + maxHistLenght) / 2, (maxHistHeight + minHistHeight) / 2), "WARNING!", fill="white")
                draw.line((histogramTime[timePlusOne], histogramData[timePlusOne], histogramTime[htime], histogramData[htime]), fill="orange")

        histogramData.pop(len(histogramTime) - 1)
        draw.rectangle((minHistLenght, maxHistHeight, minHistLenght + 27, maxHistHeight + 13), fill="black", outline="white")
        draw.text((minHistLenght + 2, maxHistHeight + 2), "{0:.2f}".format(READ_ADC[0]), fill="white")
        if READ_ADC[0]>peak[0]:            
            peak.insert(0, READ_ADC[0])
        


if __name__ == "__main__":
    device = get_device(actual_args=["--i2c-address","0x3D"])
    device2 = get_device(actual_args=["--i2c-address","0x3C"])
    
    histogramData, histogramTime = init_histogram()
    liste=[0,0]
    global HIST_VALUES
    HIST_VALUES = zeros(128)

    
    while True:

        main(device, histogramData, histogramTime,liste)
        mainhist(device2)

        time.sleep(REFRESH_INTERVAL)