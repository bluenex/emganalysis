__author__ = 'tulakan'
import linecache
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import smootingFilter

##### Initiation
windowInit = 64
## plotting list
## [0,L-Deltoid][1,L-Tricep][2,L-Biceps][3,L-Flex][4,L-Ex]
## [5,R-Deltoid][6,R-Tricep][7,R-Biceps][8,R-Flex][9,R-Ex]
plotOrder = 'all'
if plotOrder == 'all':
    plotOrder = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]  # with filtering
plotSet = [0, 0, 1]  # [nofilter, mAvg, RMS]

##### time counting
timeStart = datetime.datetime.now()

##### file section
subjectName = 'P\'A'
motorSpeed = ['0', '0_3', '0_5', '0_8', '1']
actionPlane = ['yaw', 'roll']
filename = motorSpeed[0]+actionPlane[0]+'.ASC'
# filename = '0_3yaw.ASC'

# header = linecache.getline(filename, 3) # another method to get line

##### loop through the file
data = []  # pre-allocation

f = open(filename)
for i, line in enumerate(f):
    if i == 0:
        samplingRate = line.split()  # collect frequency used
        samplingRate = int(samplingRate[0])
        # print 'samplingRate', samplingRate
    elif i == 2:
        header = line  # collect header
        # print 'header', header
    elif i > 2:
        data.append(line.split())  # collect data
# print 'last i is', dataRowNo
f.close()

dataRowNo = i-2  # number of data in row, -2 for first 2 line

##### header manipulation
splited = header.split()  # split header
jointNo = 3  # number of obj to join
loopNo = len(splited)/jointNo  # number of obj after join
finalHeader = [splited[0]]  # pre-allocation

for i in range(loopNo):
    finalHeader.append(splited[(3*i)+1]+splited[(3*i)+2]+splited[(3*i)+3])  # rearrange header
dataColNo = len(finalHeader)  # number of data in column

##### data manipulation
data = np.resize(data, (dataRowNo, dataColNo))  # 0th row is number of each data
data = data.astype(np.float)
data = abs(data)  # rectification
windowSize = windowInit  # window size for smoothing

### smoothing filter / because applying filter will cut data out the length of window size
### thus no filter data will have to be cut data out the same length as filtered data
### for the convenient of plotting
filteredData0 = data[0+(windowSize/2):-1-(windowSize/2)+1, 1:]  # no filter
filteredData1 = smootingFilter.movingAvg(windowSize, data[:, 1:])  # ignore label of data number, at data[:,0]
filteredData2 = smootingFilter.rms(windowSize, data[:, 1:])  # root mean square filter

label = []
label = data[0:dataRowNo-windowSize, 0]/samplingRate  # scaling x axis label to be sec (deviding by sampling rate)

##### plotting
plt.figure(subjectName+' - '+filename+' - '+str(windowSize))

for i in range(len(plotOrder)):
# for i in range(10):
    if len(plotOrder) != 1:
        plt.subplot(5, 2, 1+i)
    ### with filtering
    if plotSet[0] == 1:
        plt.plot(label, filteredData0[:, plotOrder[i]], 'b--', label="no filter")
    if plotSet[1] == 1:
        plt.plot(label, filteredData1[:, plotOrder[i]], 'k', linewidth=2.0, label="mAvg filter")
    if plotSet[2] == 1:
        plt.plot(label, filteredData2[:, plotOrder[i]], 'r', linewidth=2.0, label="rms filter")
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

##### time counting
timeStop = datetime.datetime.now()
totalTime = timeStop-timeStart
print 'this used', totalTime.total_seconds(), 'sec'

##### finish with show plot
# if sum(plotSet) == 1:
if len(plotOrder) == 1:
    plt.legend()
# plt.show()