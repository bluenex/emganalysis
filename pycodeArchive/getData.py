__author__ = 'tulakan'

import numpy as np
import linecache
import pickle
import os

def getHeader(rawHeader):
    ##### header manipulation
    splited = rawHeader.split()  # split header
    jointNo = 3  # number of obj to join
    loopNo = len(splited)/jointNo  # number of obj after join
    finalHeader = [splited[0]]  # pre-allocation

    for i in range(loopNo):
        finalHeader.append(splited[(3*i)+1]+splited[(3*i)+2]+splited[(3*i)+3])  # rearrange header

    return finalHeader

def getDataBack(savedir, subjectName, actionname, windowSize, filterType):
    header = pickle.load(open(os.path.join(savedir, 'header.p'), "rb"))
    fstcoldtassec = pickle.load(open(os.path.join(savedir, actionname+'_'+'fstcoldtassec.p'), "rb"))
    data = np.loadtxt(savedir+'//'+subjectName+'_'+actionname+'_'+str(windowSize)+'_'+filterType+'.txt')

    return header, fstcoldtassec, data
