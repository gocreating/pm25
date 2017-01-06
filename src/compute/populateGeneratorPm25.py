# coding=UTF-8
import sys
import logging
import glob
import os
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

SRC_dfR1Pm25Sum = '../../data/relayMetrices/dfR1Pm25Sum.csv'
SRC_dfR1WeightSum = '../../data/relayMetrices/dfR1WeightSum.csv'
SRC_dfR2Pm25Sum = '../../data/relayMetrices/dfR2Pm25Sum.csv'
SRC_dfR2WeightSum = '../../data/relayMetrices/dfR2WeightSum.csv'

DEST = '../../data/pm25.csv'
OUTPUT_CSV_COLUMNS = ['latitude', 'longitude', 'pm25', 'timestamp']

def main():
    dfR1Pm25Sum = pd.read_csv(os.path.join(SRC_dfR1Pm25Sum), index_col=0)
    dfR1WeightSum = pd.read_csv(os.path.join(SRC_dfR1WeightSum), index_col=0)
    dfR2Pm25Sum = pd.read_csv(os.path.join(SRC_dfR2Pm25Sum), index_col=0)
    dfR2WeightSum = pd.read_csv(os.path.join(SRC_dfR2WeightSum), index_col=0)

    for df in [dfR1Pm25Sum, dfR1WeightSum, dfR2Pm25Sum, dfR2WeightSum]:
        columnsToDrop = []
        for column in df:
            if 0 in df[column].values:
                columnsToDrop.append(column)
        dfR1Pm25Sum.drop(columnsToDrop, inplace=True, axis=1)
        dfR1WeightSum.drop(columnsToDrop, inplace=True, axis=1)
        dfR2Pm25Sum.drop(columnsToDrop, inplace=True, axis=1)
        dfR2WeightSum.drop(columnsToDrop, inplace=True, axis=1)

    # dfR1Pm25 = dfR1Pm25Sum / dfR1WeightSum
    # dfR2Pm25 = dfR2Pm25Sum / dfR2WeightSum
    # dfPm25 = dfR1Pm25 - dfR2Pm25

    dfR1Pm25 = dfR1Pm25Sum / dfR1WeightSum
    dfPm25 = dfR1Pm25

    dfPm25.to_csv(
        DEST,
        index=True,
    )

main()
