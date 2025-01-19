import os
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import time
from src.objects.ClusterDeleted import ClusterDeleted


def read_o_file(inDir, outDir):
    logFiles = {}
    preHeaderLine = 'Per MPI rank'
    
    for files in os.walk(inDir):
        for names in files:
            for name in names:
                if('.sh.o' in name):
                    logFiles[name.split('.sh.')[1]] = name
    
    files = []
    for key in logFiles.keys():
        print(key)
        print(logFiles[key])
        rawFile = None
        
        if(not os.path.exists(outDir)):
            os.makedirs(outDir)
            
        headerNext = False
        dataNext = False
        reactData = False
        headerWritten = False
        headers = None
        fileNo = 1
        with open(inDir + '/' + logFiles[key], 'r') as file:
            
            previousData = [-1]
            for line in file:
                reactData = True
                    
                if('Loop time' in line):
                    dataNext = False
    
                if(headerNext):
                    if(not headerWritten):
                        filePath = outDir + '/' + key + '_RAW_DATA_' + str(fileNo) + '.csv'
                        fileNo += 1
                        files.append(filePath)
                        if(os.path.isfile(filePath)):
                            rawFile = open(filePath, 'a', newline='')
                            rawFile.truncate(0)
                        else:
                            rawFile = open(filePath, 'w', newline='')
    
                        csvWriter = csv.writer(rawFile, dialect='excel', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        headers = line.strip().split()
                        csvWriter.writerow(headers)
    
                    headerNext = False
                    dataNext = True
                    if(reactData):
                        headerWritten = True
                    
                if(dataNext):
                    
                    data = line.strip().split()
                    if(data[0] == previousData[0] or data == headers or 'WARNING' in data[0]):
                        continue
                    else:
                        csvWriter.writerow(data)
                        previousData = data
                if(preHeaderLine in line):
                    headerNext = True
                    
        rawFile.close()
        df = pd.read_csv(filePath)
        return df


def read_del_file(inDir, outDir):
    logFiles = []
    
    for files in os.walk(inDir):
        for names in files:
            for name in names:
                if('.del' in name):
                    logFiles.append(name)
    
    files = []
    for file in logFiles: 
        if(not os.path.exists(outDir)):
            os.makedirs(outDir)
        timestep = {}
        
        with open(inDir + '/' + file, 'r') as file:
            for line in file:
                clustersDeleted = []
                data = line.split()
                clustersDeleted.append(ClusterDeleted(data[3], data[2]))
                
                if(data.__len__() > 4):
                    clustersDeleted.append(ClusterDeleted(data[5], data[4]))
                if(data.__len__() > 6):
                    clustersDeleted.append(ClusterDeleted(data[7], data[6]))
                if(data.__len__() > 8):
                    clustersDeleted.append(ClusterDeleted(data[9], data[8]))
                timestep[data[1]] = clustersDeleted
    return timestep

