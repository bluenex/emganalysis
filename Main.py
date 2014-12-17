__author__ = 'tulakan'
import linecache
import numpy as np
import matplotlib.pyplot as plt
import datetime

##### time counting
timeStart = datetime.datetime.now()

##### file section
subjectName = 'Aon'
filename = '0_3roll.ASC'
# filename = '0_3yaw.ASC'

# header = linecache.getline(filename, 3) # another method to get line

##### loop through the file
data = [] # pre-allocation

f = open(filename)
for i, line in enumerate(f):
    if i == 0:
        freqUsed = line.split()  # collect frequency used
        # print 'freqUsed', freqUsed
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
data = abs(data)
data[:,0] = data[:,0]/1024
# print data[:, 0]


# row = np.size(data,0)
# col = np.size(data,1)
# print row, col

# print data.dtype

##### plotting
plt.figure(subjectName+' '+filename)
plotOrder = [1, 6, 2, 7, 3, 8, 4, 9, 5, 10]
for i in range(len(plotOrder)):
# for i in range(10):
    plt.subplot(5, 2, 1+i)
    # plt.plot(data[range(np.size(data, 0)), plotOrder[i]])
    # plt.title(finalHeader[plotOrder[i]])
    plt.plot( data[:, 0], data[range(np.size(data, 0)), plotOrder[i]])
    plt.title(finalHeader[plotOrder[i]])
    # plt.plot(data[range(np.size(data, 0)), i])
    # plt.title(finalHeader[i])
# plt.tight_layout()
plt.subplots_adjust(hspace=0.35)
# plt.show()

##### time counting
timeStop = datetime.datetime.now()
totalTime = timeStop-timeStart
print 'this used', totalTime.total_seconds(), 'sec'

plt.show()



