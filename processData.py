__author__ = 'tulakan'

import numpy as np
import linecache
import getData
import smootingFilter
import os
import pickle
import datetime
import time

# subjectName = 'PA'
# motorSpeed = '1'
# actionPlane = 'roll'

# filename = '1roll.ASC'
def saveProcessed(subjectName, filename, windowInit):
    # filename = motorSpeed+actionPlane+'.ASC'
    actionname = os.path.split(filename)[-1]  # screen dir out, only pick file name
    print(filename)

    # get sampling rate
    spr = linecache.getline(filename, 1)
    spr = spr.split()[0]
    # get header
    header = linecache.getline(filename, 3)
    header = getData.getHeader(header)
    # get raw data
    rawdt = np.loadtxt(filename, skiprows=3)
    fstcoldt = rawdt[:, 0]  # first column data 1,2,3,...,len(data)
    fstcoldtassec = fstcoldt/int(spr)  # convert hertz to sec
    rawdt = rawdt[:, 1:]  # 10 channels of muscles
    # process data
    windowSize = windowInit
    fstcoldtassec = fstcoldtassec[0:-1-windowSize+1]  # cutting out the window size
    rawrecdt = abs(rawdt)  # raw data rectification
    # mavgdt = smootingFilter.movingAvg(windowSize, rawrecdt)  # moving average filtered
    # rmsdt = smootingFilter.rms(windowSize, rawrecdt)  # root mean square filted
    rawrecdt = rawrecdt[0+(windowSize/2):-1-(windowSize/2)+1, :]  # make easier to plot
    # save data
    savedir = os.path.join(subjectName, 'processed')
    if not os.path.exists(savedir):
        os.makedirs(savedir)

    # pickle.dump(header, open(os.path.join(savedir, 'header.p'), "wb"))
    # pickle.dump(fstcoldtassec, open(os.path.join(savedir,actionname+'_'+'fstcoldtassec.p'), "wb"))
    np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'rectify'+'.txt', rawrecdt)
    # np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'mAvg'+'.txt', mavgdt)
    # np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'rms'+'.txt', rmsdt)

def processAllData(windowSize):
    ##### time counting
    timeStart = datetime.datetime.now()

    ##### initiation, get subject name
    topdir = 'D:\Dropbox\Rehabilitation Project\EMG data\EMG Gyro 26-27 Aug'  # top directory to go
    excld = '[Old Data]'  # folder excluded from list
    subjtname = [x for x in os.listdir(topdir) if x != excld]  # get subject name from folder name in topdir

    # ### check for every subject folder if it contains the same number of data files
    # for i in range(len(subjtname)):  # get data file in each subject folder
    #     counter = 0
    #     for file in os.listdir(os.path.join(topdir,subjtname[i])):  # only in subject name folder (exclude edit folder)
    #         if file.endswith(".ASC"):
    #             counter += 1
    #             # print subjtname[i], file
    #     print subjtname[i], '=', counter

    datafile = [x for x in os.listdir(os.path.join(topdir, subjtname[0])) if x.endswith(".ASC")]  # data file name- 0roll.ASC

    ##### process data
    windowSize = windowSize  # window size for filtering
    for i in range(len(subjtname)):
        print i
        for j in range(len(datafile)):
            saveProcessed(subjtname[i], os.path.join(topdir, subjtname[i], datafile[j]), windowSize)

    ##### time counting
    timeStop = datetime.datetime.now()
    totalTime = timeStop-timeStart
    print 'this used', totalTime.total_seconds(), 'sec or', totalTime.total_seconds()/60, 'min'




