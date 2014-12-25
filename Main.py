__author__ = 'tulak_000'

import os
import time
import processData
import datetime
import sys
import getData
import matplotlib.pyplot as plt
import plottingdata
import numpy as np

# ##### pass all data for all subject through filter and save as txt, pickle file (takes 10 min)
# windowSize = 64
# processData.processAllData(windowSize)
# sys.exit()

##### loading data
# ['Aon', 'JongSook', 'Joy', 'Mighty', 'PA', 'PMean', 'PTook', 'Q smart', 'Zaw']
# [0, 1, 2, 3, 4, 5, 6, 7, 8]
# ['0roll.ASC', '0yaw.ASC', '0_3roll.ASC', '0_3yaw.ASC', '0_5roll.ASC', '0_5yaw.ASC', '0_8roll.ASC', '0_8yaw.ASC', '1roll.ASC', '1yaw.ASC']
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# ['N', 'L-Deltoid(uV)', 'L-Tricep(uV)', 'L-Bicep(uV)', 'L-Flex(uV)', 'L-Ex(uV)', 'R-Deltoid(uV)', 'R-Tricep(uV)', 'R-Bicep(uV)', 'R-Flex(uV)', 'R-Ex(uV)']
# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
subjectName = 'Aon'
actionname1 = '1roll.ASC'
musclename = 7
windowSize = 64
filterType = 'rms'  # ['rectify', 'mAvg', 'rms']
savedir = os.path.join(subjectName, 'processed')
[header, fstcoldtassecAon0roll64, dataAon0roll64LDel] = getData.getDataBack(savedir, subjectName, actionname1, windowSize, filterType)
print np.max(dataAon0roll64LDel,axis=0)
#
# subjectName = 'Aon'
actionname2 = '1yaw.ASC'
# musclename = 7
# windowSize = 64
# filterType = ['rectify', 'mAvg', 'rms']
# filterType = 'rms'  # ['rectify', 'mAvg', 'rms']
# savedir = os.path.join(subjectName, 'processed')
[header, fstcoldtassecAon1roll64, dataAon1roll64LDel] = getData.getDataBack(savedir, subjectName, actionname2, windowSize, filterType)
print np.max(dataAon1roll64LDel,axis=0)

##### single muscle plot
# fgn = plottingdata.figurename()
# plt.figure(subjectName+actionname1+'vs'+actionname2+str(windowSize)+filterType)
# plottingdata.singlePlot(actionname1[0:-4], musclename, fstcoldtassecAon0roll64, dataAon0roll64LDel, 'b')
# plottingdata.singlePlot(actionname2[0:-4], musclename, fstcoldtassecAon1roll64, dataAon1roll64LDel, 'r')
# plt.title(header2[musclename])
# plt.legend()
# plt.show()

fg1 = plottingdata.figurename([subjectName,actionname1[0:-4],'vs',actionname2[0:-4],str(windowSize),filterType])

plt.figure(fg1)
# concatenate data to find max value of y axis
dataAon = np.concatenate((dataAon0roll64LDel,dataAon1roll64LDel), axis=0)
maxY = np.max(dataAon, axis=0)

for i in range(5):
    if maxY[i] > maxY[i+5]:
        maxY[i+5] = maxY[i]
    elif maxY[i] < maxY[i+5]:
        maxY[i] = maxY[i+5]

plottingdata.plotall(actionname2[0:-4], header, fstcoldtassecAon1roll64, dataAon1roll64LDel, 'b', maxY)
plottingdata.plotall(actionname1[0:-4], header, fstcoldtassecAon0roll64, dataAon0roll64LDel, 'r', maxY)


plt.show()
