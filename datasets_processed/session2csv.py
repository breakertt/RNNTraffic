# -*- coding: utf-8 -*-ds

import os, sys
from pathlib import Path
import pandas as pd
import numpy as np
import math
from PIL import Image

SAMPLE_LENGTH_MAX = 1500
SAMPLE_LENGTH_MIN = 300

def handleSession(pcapFile):
    pcap = np.fromfile(pcapFile, np.uint8)
    if len(pcap) < SAMPLE_LENGTH_MIN:
        return (False, None)
    elif len(pcap) >= SAMPLE_LENGTH_MAX:
        pcap = pcap[:SAMPLE_LENGTH_MAX]
    else:
        pcap = np.resize(pcap, (SAMPLE_LENGTH_MAX, ))
    return (True, pcap)

def handleFolder(dir, filenames):
    pcapFiles = list(filter(lambda filename: os.path.splitext(filename)[1] == ".pcap", files))
    if len(pcapFiles) == 0:
        return

    csvDir = str(Path(dir).parents[0])
    dirBasename = os.path.basename(dir)
    csvFilename = dirBasename + ".csv"
    csvFullname = csvDir + os.path.sep + csvFilename
    csvLabel = csvDir.split(os.path.sep)[-1]

    pcapFiles = [str(Path(dir) / pcapFile) for pcapFile in pcapFiles]

    print("Converting pcap sessions under {} to a single csv ({})".format(dir, csvFullname))

    csvMatrix = np.empty((0, SAMPLE_LENGTH_MAX), np.uint8)
    for pcapFile in pcapFiles:
        (isValidSessionData, sessionData) = handleSession(pcapFile)
        if isValidSessionData:
            csvMatrix = np.append(csvMatrix, np.array([sessionData]), axis=0)

    csvDataframe = pd.DataFrame(data=csvMatrix[0:,0:],
        index=[i for i in range(csvMatrix.shape[0])],
        columns=['DataIndex_'+str(i) for i in range(csvMatrix.shape[1])])

    csvDataframe['Label'] = csvLabel
    csvDataframe.to_csv(csvFullname)

if __name__ == "__main__":
    print("Current working directory: {}".format(os.getcwd()))

    rootdir = os.getcwd()
    for root, subdirs, files in os.walk(rootdir):
        handleFolder(root, files)
