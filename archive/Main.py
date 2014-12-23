__author__ = 'tulakan'
import linecache
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import smootingFilter, getData, plottingData

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
filename = motorSpeed[4]+actionPlane[0]+'.ASC'
# filename = '0_3yaw.ASC'

##### get data
[data, samplingRate, finalHeader, dataRowNo, dataColNo] = getData.getDataFromFile(filename)
data = abs(data)  # rectification

### smoothing filter / because applying filter will cut data out the length of window size
### thus no filter data will have to be cut data out the same length as filtered data
### for the convenient of plotting
windowSize = windowInit  # window size for smoothing
filteredData0 = data[0+(windowSize/2):-1-(windowSize/2)+1, 1:]  # no filter
filteredData1 = smootingFilter.movingAvg(windowSize, data[:, 1:])  # ignore label of data number, at data[:,0]
filteredData2 = smootingFilter.rms(windowSize, data[:, 1:])  # root mean square filter
# print np.max(filteredData2)
# sys.exit()
# np.savetxt('[rec]'+subjectName+filename, filteredData0)
# np.savetxt('[mAvg]'+subjectName+filename, filteredData1)
# np.savetxt('[rms]'+subjectName+filename, filteredData2)

label = []
label = data[0:dataRowNo-windowSize, 0]/samplingRate  # scaling x axis label to be sec (deviding by sampling rate)

plottingData.plotEMG(plotSet, plotOrder, filteredData0, filteredData1, filteredData2, finalHeader, label, subjectName, filename, windowSize)

##### time counting
timeStop = datetime.datetime.now()
totalTime = timeStop-timeStart
print 'this used', totalTime.total_seconds(), 'sec'

##### finish with show plot
# if sum(plotSet) == 1:
if len(plotOrder) == 1:
    plt.legend()
plt.show()