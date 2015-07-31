__author__ = 'tulakan'

import numpy as np
import matplotlib.pyplot as plt

def plotEMG(plotSet, plotOrder, filteredData0, filteredData1, filteredData2, finalHeader, label, subjectName, filename, windowSize):

    ##### plotting
    plt.figure(subjectName+' - '+filename+' - '+str(windowSize))

    for i in range(len(plotOrder)):
    # for i in range(10):
        if len(plotOrder) != 1:
            plt.subplot(5, 2, 1+i)
        ### with filtering
        if plotSet[0] == 1:
            plt.plot(label, filteredData0[:, plotOrder[i]], 'b--', label="no filter")
            tempY = np.max(filteredData0)
            yMAX = np.around(tempY, decimals=-2)
            if tempY > yMAX:
                yMAX += 50
            plt.ylim(ymax=yMAX)
        if plotSet[1] == 1:
            plt.plot(label, filteredData1[:, plotOrder[i]], 'k', linewidth=2.0, label="mAvg filter")
            tempY = np.max(filteredData1)
            yMAX = np.around(tempY, decimals=-2)
            if tempY > yMAX:
                yMAX += 50
            plt.ylim(ymax=yMAX)
        if plotSet[2] == 1:
            plt.plot(label, filteredData2[:, plotOrder[i]], 'g', linewidth=2.0, label="rms filter")
            tempY = np.max(filteredData2)
            yMAX = np.around(tempY, decimals=-2)
            if tempY > yMAX:
                yMAX += 50
            plt.ylim(ymax=yMAX)
        plt.title(finalHeader[plotOrder[i]+1])
        plt.xlim(xmax=label[-1])
        plt.xlabel('Time (sec)')
        plt.ylabel('Voltage (uV)')
        ### basic structure
        # plt.plot(data[range(np.size(data
        # , 0)), i])
        # plt.title(finalHeader[i])
    # plt.tight_layout()  # tighten subplot layout
    plt.subplots_adjust(hspace=0.45)  # more specific that tight
    # [xmin, xmax] = plt.xlim()   # return the current xlim

