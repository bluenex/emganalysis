__author__ = 'tulakan'

import numpy as np
import linecache
import getData
import smootingFilter
import os
import cPickle
import datetime
import time

# subjectName = 'PA'
# motorSpeed = '1'
# actionPlane = 'roll'

# filename = '1roll.ASC'

def saveProcessed(filename, savedir, windowSize):
    # filename = motorSpeed+actionPlane+'.ASC'
    filenameSplit = (os.path.split(filename)[-1]).split(".")[0]
    # actionname = os.path.split(filename)[-1]  # screen dir out, only pick file name
    # print filenameSplit

    # get sampling rate
    print "get sampling rate.."
    spr = linecache.getline(filename, 1)
    spr = spr.split()[0]
    print "DONE"
    # print spr
    # get header
    print "get header.."
    header = linecache.getline(filename, 3)
    header = getData.getHeader(header)
    print "DONE"
    # print header
    time.sleep(1)
    # get raw data
    print "get raw data.."
    rawdt = np.loadtxt(filename, skiprows=3)
    fstcoldt = rawdt[:, 0]  # first column data 1,2,3,...,len(data)
    fstcoldtassec = fstcoldt/int(spr)  # convert hertz to sec
    rawdt = rawdt[:, 1:]  # 10 channels of muscles
    print "DONE"

    # process data
    fstcoldtassec = fstcoldtassec[0:-1-windowSize+1]  # cutting out the window size
    print "rectify data.."
    rawrecdt = abs(rawdt)  # raw data rectification
    print "DONE"
    print "applying moving average filter.."
    mavgdt = smootingFilter.movingAvg(windowSize, rawrecdt)  # moving average filtered
    print "DONE"
    print "applying root mean square filter.."
    rmsdt = smootingFilter.rms(windowSize, rawrecdt)  # root mean square filted
    print "DONE"
    rawrecdt = rawrecdt[0+(windowSize/2):-1-(windowSize/2)+1, :]  # make easier to plot

    # save data
    # savedir = os.path.join(subjectName, 'processed')
    # if not os.path.exists(savedir):
    #     os.makedirs(savedir)
    print "dump filtered data to pickle files.."
    cPickle.dump(header, open(os.path.join(savedir, 'header.p'), "wb"))
    cPickle.dump(fstcoldtassec, open(os.path.join(savedir, 'fstcoldtassec.p'), "wb"))
    cPickle.dump(rawrecdt, open(os.path.join(savedir, filenameSplit + "_" + str(windowSize) + "_rectify.p"), "wb"))
    print "rectify DONE"
    cPickle.dump(mavgdt, open(os.path.join(savedir, filenameSplit + "_" + str(windowSize) + "_mAvg.p"), "wb"))
    print "moving average DONE"
    cPickle.dump(rmsdt, open(os.path.join(savedir, filenameSplit + "_" + str(windowSize) + "_rms.p"), "wb"))
    print "root mean square DONE"
    # np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'rectify'+'.txt', rawrecdt)
    # np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'mAvg'+'.txt', mavgdt)
    # np.savetxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+'rms'+'.txt', rmsdt)

# def processAllData(dataDir, windowSize):
#     ##### time counting
#     timeStart = datetime.datetime.now()
#
#     ##### initiation, get subject name
#     topdir = 'D:\Dropbox\Rehabilitation Project\EMG data\EMG Gyro 26-27 Aug'  # top directory to go
#     excld = '[Old Data]'  # folder excluded from list
#     subjtname = [x for x in os.listdir(topdir) if x != excld]  # get subject name from folder name in topdir
#
#     # ### check for every subject folder if it contains the same number of data files
#     # for i in range(len(subjtname)):  # get data file in each subject folder
#     #     counter = 0
#     #     for file in os.listdir(os.path.join(topdir,subjtname[i])):  # only in subject name folder (exclude edit folder)
#     #         if file.endswith(".ASC"):
#     #             counter += 1
#     #             # print subjtname[i], file
#     #     print subjtname[i], '=', counter
#
#     datafile = [x for x in os.listdir(os.path.join(topdir, subjtname[0])) if x.endswith(".ASC")]  # data file name- 0roll.ASC
#
#     ##### process data
#     windowSize = windowSize  # window size for filtering
#     for i in range(len(subjtname)):
#         print i
#         for j in range(len(datafile)):
#             saveProcessed(subjtname[i], os.path.join(topdir, subjtname[i], datafile[j]), windowSize)
#
#     ##### time counting
#     timeStop = datetime.datetime.now()
#     totalTime = timeStop-timeStart
#     print 'this used', totalTime.total_seconds(), 'sec or', totalTime.total_seconds()/60, 'min'
