import os
import time
import datetime
import sys
import getData
import matplotlib.pyplot as plt
import plottingdata
import numpy as np
import cPickle
import linecache

# setting variables
dataPath = "/Users/tulakan/OneDrive/BME/Rehabilitation Project/EMG data/EMG Gyro 22-23 Jul 2015"  # raw data dir
subjectName = "*"  # * for all
processedFolderName = "Processed"
processedPath = os.path.join(dataPath, processedFolderName, subjectName)  # processed data dir
printSubjtName = False
printDataFileName = "No"
windowSize = 64

# loop through directory -> get folder name for each subject and raw data file names
allSubject = [x for x in os.listdir(dataPath) if not x.startswith(".") and x != processedFolderName]
if printSubjtName: print allSubject

# data file names for each subject is collected as dictionary
dataFileName = {x: [i for i in os.listdir(os.path.join(dataPath, x)) if not i.startswith(".") and i.endswith(".ASC")]  for x in allSubject}
if printDataFileName != "No":
    try:
        print dataFileName[printDataFileName]
    except KeyError:
        print "No data for", printDataFileName


def main():

    # # check if there is processed data
    # checkProcessedIfExist()
    # process and save all data
    processAll()


def checkProcessedIfExist():
    if not os.path.exists(os.path.join(dataPath, "Processed")):
        os.makedirs(os.path.join(dataPath, "Processed"))
    for x in allSubject:
        if not os.path.exists(os.path.join(dataPath, "Processed", x)):
            os.makedirs(os.path.join(dataPath, "Processed", x))
    for x in allSubject:
        # .p is pickle files for processed data
        # this snippet trying to find .p in processed folder
        # if found it shows files name
        # else print no .p file in current dir
        if len([i for i in os.listdir(os.path.join(dataPath, processedFolderName, x)) if i.endswith(".p")]) == 0:
            print "no .p file in", os.path.join(dataPath, processedFolderName, x)
        else:
            print x, ":", [i for i in os.listdir(os.path.join(dataPath, processedFolderName, x)) if i.endswith(".p")]
        # for y in dataFileName[x]:
        # if not os.path.exists(os.path.join(dataPath, processedFolderName, x, y.split(".")[0]+"_processed.p")):
        #     print y.split(".")[0]+"_processed.p", "does not exist.."
        # print os.path.join(dataPath, allSubject[0], dataFileName[allSubject[0]][0])


def processAll():
    # process data
    savePath = os.path.join(dataPath, processedFolderName)
    # count time
    startTime = datetime.datetime.now()

    for i in allSubject:
        savedir = os.path.join(savePath, i)
        print "#########################"
        print "processing", i + "..."
        print "#########################"
        for j in dataFileName[i]:
            saveProcessed(os.path.join(dataPath, i, j), savedir, windowSize)
            print "#########################"
            print j, "process - DONE"
            print "#########################"

    # savedir = os.path.join(savePath, allSubject[0])
    # processData.saveProcessed(os.path.join(dataPath, allSubject[0], dataFileName[allSubject[0]][0]), savedir, windowSize)

    # count time
    stopTime = datetime.datetime.now()
    print "data processing takes", stopTime-startTime


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
    mavgdt = movingAvgFilter(windowSize, rawrecdt)  # moving average filtered
    print "DONE"
    print "applying root mean square filter.."
    rmsdt = rmsFilter(windowSize, rawrecdt)  # root mean square filted
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


# filter functions

# These filters will move window over data starting at data position of (window size/2)
# so that data loss will be divided to be half for initial and half for terminal

def movingAvgFilter(windowSize, data):
    startPoint = windowSize/2  # position to start windowing
    noOfData = np.size(data, 0)
    dataCol = np.size(data, 1)

    newData = np.zeros((noOfData-windowSize, dataCol))  # -1 to ignore data[:,1]
    for i in range(startPoint, noOfData-startPoint):
        newData[i-startPoint, :] = (sum(data[i-startPoint:i+startPoint, :]))/windowSize
    return newData


def rmsFilter(windowSize, data):
    startPoint = windowSize/2  # position to start windowing
    noOfData = np.size(data, 0)
    dataCol = np.size(data, 1)

    newData = np.zeros((noOfData-windowSize, dataCol))  # -1 to ignore data[:,1]
    for i in range(startPoint, noOfData-startPoint):
        newData[i-startPoint, :] = np.sqrt(sum(data[i-startPoint:i+startPoint, :]**2))/np.sqrt(windowSize)
    return newData


# call main function
main()
