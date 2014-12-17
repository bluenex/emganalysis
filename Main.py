__author__ = 'tulakan'
import linecache
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import smootingFilter

##### time counting
timeStart = datetime.datetime.now()

##### file section
subjectName = 'Aon'
# filename = '0_3roll.ASC'
filename = '0_3yaw.ASC'

# header = linecache.getline(filename, 3) # another method to get line

##### loop through the file
data = [] # pre-allocation

f = open(filename)
for i, line in enumerate(f):
    if i == 0:
        samplingRate = line.split()  # collect frequency used
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
dataColNo = len(finalHeader) # number of data in column

##### data manipulation
data = np.resize(data, (dataRowNo, dataColNo))  # 0th row is number of each data
data = data.astype(np.float)
# data = abs(data)  # rectification
windowSize = 100  # window size for smoothing
# data[:, 0] = data[:, 0]/1024  # scaling label to be sec

### smoothing filter
# filteredData = smootingFilter.movingAvg(windowSize, data[:, 1:])  # ignore label of data number, data[:,0]
filteredData = smootingFilter.rms(windowSize, data[:, 1:])

label = []
label = data[0:dataRowNo-windowSize, 0]/1024  # scaling label to be sec

# newdtRow = np.size(newData, 0)
# newdtCol = np.size(newData, 1)
# print 'row = %d, col = %d' % (newdtRow, newdtCol)
# print 'start data', newData[0, :]
#
# print 'end data', newData[-1:-10:-1, :]

# windowSize = 32
# startPoint = windowSize/2 # 16
# print 'startPoint[%d]' % startPoint, data[startPoint-1, 1:6]
# print 'window initial point[%s]' % str(startPoint-startPoint), data[startPoint-startPoint, 1:6]
# print 'window terminal point[%s]' % str(startPoint+startPoint-1), data[startPoint+startPoint-1, 1:6]
# print 'sum value no parentheses', sum(data[startPoint-startPoint:startPoint+startPoint-1, 1:6])/windowSize
# print 'sum value with parentheses', (sum(data[startPoint-startPoint:startPoint+startPoint-1, 1:6]))/windowSize
# print data[:,1:]

# row = np.size(data,0)
# col = np.size(data,1)
# print row, col

# print data.dtype

##### plotting
plt.figure(subjectName+' - '+filename+' - '+str(windowSize))

# plotOrder = [1, 6, 2, 7, 3, 8, 4, 9, 5, 10]  # without filtering
plotOrder = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]  # with filtering
for i in range(len(plotOrder)):
# for i in range(10):
    plt.subplot(5, 2, 1+i)
    ### without filtering
    # plt.plot(data[:, 0], data[range(np.size(data, 0)), plotOrder[i]])
    # plt.title(finalHeader[plotOrder[i]])
    ### with filtering
    plt.plot(label, filteredData[:, plotOrder[i]])
    plt.title(finalHeader[plotOrder[i]+1])
    plt.xlim(xmax=label[-1])
    plt.xlabel('Time (sec)')
    plt.ylabel('Voltage (uV)')
    ### basic structure
    # plt.plot(data[range(np.size(data, 0)), i])
    # plt.title(finalHeader[i])
# plt.tight_layout()  # tighten subplot layout
plt.subplots_adjust(hspace=0.45)  # more specific that tight
# [xmin, xmax] = plt.xlim()   # return the current xlim

##### time counting
timeStop = datetime.datetime.now()
totalTime = timeStop-timeStart
print 'this used', totalTime.total_seconds(), 'sec'

##### finish with show plot
plt.show()



