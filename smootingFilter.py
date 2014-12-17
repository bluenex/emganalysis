__author__ = 'tulakan'

import numpy as np
import time

##----- These filters will move window over data starting at data position of (window size/2)
##----- so that data loss will be divided in half for initial and half for terminal

def movingAvg(windowSize, data):
    startPoint = windowSize/2  # position to start windowing, -1 for indexing
    noOfData = np.size(data, 0)
    dataCol = np.size(data, 1)
    # print 'datasize 1 before', dataCol
    # print 'datasize 0 before', noOfData
    # print 'row = %d, col = %d' % (noOfData, dataCol)
    # print 'datasize 0 - windowsize = %d' % (noOfData-windowSize)
    newData = np.zeros((noOfData-windowSize, dataCol))  # -1 to ignore data[:,1]
    # newData = data[startPoint-1:noOfData-startPoint-1, :]   # is equal to data[startPoint-1, :]
    # newdtRow = np.size(newData, 0)
    # newdtCol = np.size(newData, 1)
    # print 'datasize 1 after', newdtCol
    # print 'datasize 0 after', newdtRow
    # print 'row = %d, col = %d' % (newdtRow, newdtCol)
    # print 'noOfData-startPoint-1 =', noOfData-startPoint-1
    for i in range(startPoint, noOfData-startPoint):
        newData[i-startPoint, :] = (sum(data[i-startPoint:i+startPoint, :]))/windowSize
    return newData

def rms(windowSize, data):
    startPoint = windowSize/2  # position to start windowing