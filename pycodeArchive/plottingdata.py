__author__ = 'tulakan'

import os
import time
import processData
import datetime
import pickle
import matplotlib.pyplot as plt
import numpy as np
import sys
import getData

# ##### time counting
# timeStart = datetime.datetime.now()
#
# ##### initiation, get subject name
# topdir = 'D:\Dropbox\Rehabilitation Project\EMG data\EMG Gyro 26-27 Aug'  # top directory to go
# excld = '[Old Data]'  # folder excluded from list
# subjtname = [x for x in os.listdir(topdir) if x != excld]  # get subject name from folder name in topdir
# datafile = [x for x in os.listdir(os.path.join(topdir, subjtname[0])) if x.endswith(".ASC")]  # data file name- 0roll.ASC
#
# ##### loading data
# # ['Aon', 'JongSook', 'Joy', 'Mighty', 'PA', 'PMean', 'PTook', 'Q smart', 'Zaw']
# # [0, 1, 2, 3, 4, 5, 6, 7, 8]
# # subjectName = subjtname[0]
# subjectName = 'Aon'
# # ['0roll.ASC', '0yaw.ASC', '0_3roll.ASC', '0_3yaw.ASC', '0_5roll.ASC', '0_5yaw.ASC', '0_8roll.ASC', '0_8yaw.ASC', '1roll.ASC', '1yaw.ASC']
# # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# # actionname = datafile[0]
# actionname = '0roll.ASC'
# # ['L-Deltoid(uV)', 'L-Tricep(uV)', 'L-Bicep(uV)', 'L-Flex(uV)', 'L-Ex(uV)', 'R-Deltoid(uV)', 'R-Tricep(uV)', 'R-Bicep(uV)', 'R-Flex(uV)', 'R-Ex(uV)']
# # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# musclename = 8
# windowSize = 64
# filterType = ['rectify', 'mAvg', 'rms']
# filterType = filterType[2]
# savedir = os.path.join(subjectName, 'processed')
#
# # print os.path.join(savedir, 'header.p')
#
# [header, fstcoldtassecAon0roll64, dataAon0roll64] = getData.getDataBack(savedir, subjectName, actionname, windowSize, filterType)
# print 'muscle picked is', header[musclename]
#
# print 'action picked is', actionname[0:-4]
# # 2nd action picked
# actionname = datafile[8]
# print 'action picked is', actionname[0:-4]
#
# [header, fstcoldtassecAon1roll64, dataAon1roll64] = getData.getDataBack(savedir, subjectName, actionname, windowSize, filterType)
#
# # if len(fstcoldtassecAon0roll64) > len(fstcoldtassecAon1roll64):
# #     fstcoldtassec = fstcoldtassecAon0roll64
# # else:
# #     fstcoldtassec = fstcoldtassecAon1roll64
#
# # plt.figure(subjectName+)
def singlePlot(actionname, musclename, fstcoldtassec, data, color):
    plt.plot(fstcoldtassec, data[:, musclename-1], color, label=actionname)
    tempY = np.max(data)
    yMAX = np.around(tempY, decimals=-2)
    if tempY > yMAX:
        yMAX += 50
    plt.ylim(ymax=yMAX)

def plotall(actionname, header, fstcoldtassec, data, color, tempY):
    plotOrder = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    for i in range(len(plotOrder)):
    # for i in range(10):
        plt.subplot((np.size(data, 1)/2), 2, 1+i)
        plt.plot(fstcoldtassec, data[:, plotOrder[i]], color, label=actionname)
        # tempY = np.max(data[:, plotOrder[i]])
        yMAX = np.around(tempY[plotOrder[i]], decimals=-2)
        if tempY[plotOrder[i]] > yMAX:
            yMAX += 50
        plt.ylim(ymax=yMAX)
        plt.title(header[plotOrder[i]+1])
        plt.xlim(xmax=fstcoldtassec[-1])
        plt.xlabel('Time (sec)')
        plt.ylabel('Voltage (uV)')
        ### basic structure
        # plt.plot(data[range(np.size(data
        # , 0)), i])
        # plt.title(finalHeader[i])
        plt.legend()
    # plt.tight_layout()  # tighten subplot layout
    plt.subplots_adjust(hspace=0.45)  # more specific that tight
    # [xmin, xmax] = plt.xlim()   # return the current xlim

def figurename(inputlist):
    joinedname = ''
    s = ' '  # spacing
    for i in range(len(inputlist)):
        joinedname = joinedname+inputlist[i]+s
    return joinedname

# ##### time counting
# timeStop = datetime.datetime.now()
# totalTime = timeStop-timeStart
# print 'this used', totalTime.total_seconds(), 'sec'
#
# # ##### end by show plot
# plt.show()
