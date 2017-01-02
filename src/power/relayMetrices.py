# coding=UTF-8
import sys
import logging
import glob
import os
import pandas as pd
from pandas.compat import u
import numpy as np
from math import radians, cos, sin, asin, sqrt

DEFAULT_SRC_PM25 = '../../data/pm25/reducedCsvs.csv'
DEFAULT_SRC_POWER_NAME_MAP = '../../data/power/nameMap.csv'
DEFAULT_DEST_DIR = '../../data/lookupMetrices'
INPUT_PM25_CSV_COLUMNS = ['latitude', 'longitude', 'pm25', 'timestamp']
INPUT_POWER_NAME_MAP_CSV_COLUMNS = ['name', 'latitude', 'longitude']
OUTPUT_CSV_COLUMNS = ['latitude', 'longitude', 'pm25', 'timestamp']

def haversine(lat1, lon1, lat2, lon2):
	'''
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)
	'''
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c
	return km

def gaussian(x, mu, sig):
	return (1. / (sig * np.sqrt(2 * np.pi))) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
	# return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussianLatLon(lat1, lon1, lat2, lon2, radius):
	distance = haversine(lat1, lon1, lat2, lon2)

	if distance > radius:
		return 0

	return gaussian(distance, 0, radius / 3.)

def main():
    r1 = float(sys.argv[1])
    r2 = float(sys.argv[2])

    dfPm25 = pd.read_csv(
        os.path.join(DEFAULT_SRC_PM25),
        dtype={
            'latitude': np.float64,
            'longitude': np.float64,
        },
        names=INPUT_PM25_CSV_COLUMNS
    )
    dfPowerNameMap = pd.read_csv(
        os.path.join(DEFAULT_SRC_POWER_NAME_MAP),
        dtype={
            'latitude': np.float64,
            'longitude': np.float64,
        },
        names=INPUT_POWER_NAME_MAP_CSV_COLUMNS
    )

    timestamps = []
    for date in range(17, 24):
        for h in range(0, 24):
            for m in range(0, 6):
                timestamps.append('2016/12/%02d %02d:%02d' % (date, h, m * 10))
    dfR1Pm25Sum = pd.DataFrame(
        0,
        index=timestamps,
        columns=dfPowerNameMap.index.values,
        dtype=float
    )
    dfR1WeightSum = pd.DataFrame(
        0,
        index=timestamps,
        columns=dfPowerNameMap.index.values,
        dtype=float
    )
    dfR2Pm25Sum = pd.DataFrame(
        0,
        index=timestamps,
        columns=dfPowerNameMap.index.values,
        dtype=float
    )
    dfR2WeightSum = pd.DataFrame(
        0,
        index=timestamps,
        columns=dfPowerNameMap.index.values,
        dtype=float
    )

    i = 0
    for pm25Row in dfPm25[0:50].itertuples():
        i = i + 1
        if i % 50 == 0:
            print i
            # print '==============dfR1Pm25Sum==================='
            # print dfR1Pm25Sum
            # print '==============dfR1WeightSum==============='
            # print dfR1WeightSum
            # print '==============dfR2Pm25Sum================='
            # print dfR2Pm25Sum
            # print '==============dfR2WeightSum=============='
            # print dfR2WeightSum

        j = 0
        for powerRow in dfPowerNameMap.itertuples():
            weightR1 = gaussianLatLon(powerRow.latitude, powerRow.longitude, pm25Row.latitude, pm25Row.longitude, r1)
            weightR2 = gaussianLatLon(powerRow.latitude, powerRow.longitude, pm25Row.latitude, pm25Row.longitude, r2)
            dfR1Pm25Sum.loc[pm25Row.timestamp][j] = dfR1Pm25Sum.loc[pm25Row.timestamp][j] + weightR1 * pm25Row.pm25
            dfR1WeightSum.loc[pm25Row.timestamp][j] = dfR1WeightSum.loc[pm25Row.timestamp][j] + weightR1
            dfR2Pm25Sum.loc[pm25Row.timestamp][j] = dfR2Pm25Sum.loc[pm25Row.timestamp][j] + weightR2 * pm25Row.pm25
            dfR2WeightSum.loc[pm25Row.timestamp][j] = dfR2WeightSum.loc[pm25Row.timestamp][j] + weightR2
            j = j + 1

    dfR1Pm25Sum.to_csv(
        os.path.join(DEFAULT_DEST_DIR, 'dfR1Pm25Sum.csv'),
        index=True,
        header=dfPowerNameMap.name.values
    )
    dfR1WeightSum.to_csv(
        os.path.join(DEFAULT_DEST_DIR, 'dfR1WeightSum.csv'),
        index=True,
        header=dfPowerNameMap.name.values
    )
    dfR2Pm25Sum.to_csv(
        os.path.join(DEFAULT_DEST_DIR, 'dfR2Pm25Sum.csv'),
        index=True,
        header=dfPowerNameMap.name.values
    )
    dfR2WeightSum.to_csv(
        os.path.join(DEFAULT_DEST_DIR, 'dfR2WeightSum.csv'),
        index=True,
        header=dfPowerNameMap.name.values
    )

main()
