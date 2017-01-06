# coding=UTF-8
import sys
import logging
import glob
import os
import pandas as pd
import numpy as np
from sklearn import linear_model

SRC_PM25 = '../../data/pm25.csv'
SRC_POWER_RAW = '../../data/power/raw.csv'
INPUT_POWER_RAW_CSV_COLUMNS = ['name', 'latitude', 'longitude', 'load', 'timestamp']
DEST = '../../data/computed.csv'
OUTPUT_CSV_COLUMNS = ['name', 'rate']

def main():
    dfPm25 = pd.read_csv(os.path.join(SRC_PM25), index_col=0)
    dfPowerRaw = pd.read_csv(
        os.path.join(SRC_POWER_RAW),
        names=INPUT_POWER_RAW_CSV_COLUMNS,
    )
    dfResult = pd.DataFrame(columns=OUTPUT_CSV_COLUMNS)

    i = 0
    for name in dfPm25[:1]:
        i = i + 1
        loads = []
        pm25s = []
        for record in dfPm25.itertuples():
            dfFiltered = dfPowerRaw[
                (dfPowerRaw.name == name) &
                (dfPowerRaw.timestamp == record.Index)
            ]
            if len(dfFiltered) == 0:
                # print name, record.Index
                continue
            load = float(dfFiltered.load.values[0].replace('%', ''))
            pm25s.append(record[i])
            loads.append([load])
        model = linear_model.LinearRegression()
        model.fit(loads, pm25s)
        print name, model.coef_[0]
        dfResult.loc[len(dfResult)] = [name, model.coef_[0]]

    dfResult.to_csv(DEST, index=False)

main()
