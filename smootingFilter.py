__author__ = 'tulakan'

import numpy as np
import time

##----- These filters will move window over data starting at data position of (window size/2)
##----- so that data loss will be divided to be half for initial and half for terminal


def movingAvg(windowSize, data):
    startPoint = windowSize/2  # position to start windowing
    noOfData = np.size(data, 0)
    dataCol = np.size(data, 1)

    newData = np.zeros((noOfData-windowSize, dataCol))  # -1 to ignore data[:,1]
    for i in range(startPoint, noOfData-startPoint):
        newData[i-startPoint, :] = (sum(data[i-startPoint:i+startPoint, :]))/windowSize
    return newData


def rms(windowSize, data):
    startPoint = windowSize/2  # position to start windowing
    noOfData = np.size(data, 0)
    dataCol = np.size(data, 1)

    newData = np.zeros((noOfData-windowSize, dataCol))  # -1 to ignore data[:,1]
    for i in range(startPoint, noOfData-startPoint):
        newData[i-startPoint, :] = np.sqrt(sum(data[i-startPoint:i+startPoint, :]**2))/np.sqrt(windowSize)
    return newData