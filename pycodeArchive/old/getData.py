__author__ = 'tulakan'

import numpy as np

def getDataFromFile(filename):

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

    return data, samplingRate, finalHeader, dataRowNo, dataColNo

