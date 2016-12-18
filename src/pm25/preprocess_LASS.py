# -*- coding: utf-8 -*-

import sys
import glob
import os
import time
import datetime

csvFileDict = dict()

def preProcessLogFile(logFileName, csvFolderPath, debugLogFile):
	fileName = logFileName.split('\\')[1]
	print('Reading: <' + fileName + '>')
	
	lineCounter = 0
	dataCounter = 0
	filteredCounter = 0
	errCounter = 0
	
	rawlogfile = open(logFileName, "r")
	
	print '=================== Start parsing file: %s ===================' % (fileName)
	if debugLogFile is not None:
		debugLogFile.write('=================== Start parsing file: %s ===================\n\n' % (fileName))
	
	startTime = time.time()
	
	for unhandledline in rawlogfile.readlines():
		line = unhandledline.strip()
		
		lineCounter += 1
		if lineCounter % 1000 == 0:
			print '.',
		if lineCounter % 100000 == 0:
			print ''
		
		# not empty line
		if line:
		
			# Split attributes
			attrs = line.split("|")
			attrDict = {'device_msg':attrs[0]}
			
			# Data contained line
			if len(attrs) != 1:
				for attr in attrs[1:]:
				
					# not empty column(...||...)
					if attr:
						splitedAttr = attr.split("=")
						
						try:
							# must has '=' mark (...|ex|...)
							# not a number data in attr (...|ex='NaN'|...)
							# no data in attr (...|ex=|...)
							if len(	splitedAttr) != 1 and \
									splitedAttr[1].lower() != "nan" and splitedAttr[1].lower() != "na" and splitedAttr[1].lower() != " nan" and splitedAttr[1].lower() != "none" and \
									splitedAttr[1]:
								attrDict[splitedAttr[0]] = splitedAttr[1]
								
						except Exception as err:
							# dictionary data failed
							print '*',
							errCounter += 1
							if debugLogFile is not None:
								debugLogFile.write('******************* Error at %d *******************\n\n%s\n\n%s\n\nattr: %s\n\ndata length: %d\n\n\n' % (lineCounter, line, err, attr, len(splitedAttr)))
				
				PM25 = 0.0
				try:
					if ('PM2_5' in attrDict):
						PM25 = float(attrDict['PM2_5'])
					if ('s_d0' in attrDict):
						PM25 = float(attrDict['s_d0'])
				except Exception :
					pass
					
				if( PM25 > 0.0 and \
					'date' in attrDict and \
					'time' in attrDict and \
					'gps_lat' in attrDict and \
					'gps_lon' in attrDict and \
					attrDict['gps_lat'] != 0 and\
					attrDict['gps_lon'] != 0):
					
					try:
						logDateTime = datetime.datetime.strptime('%s %s' % (attrDict['date'], attrDict['time']), "%Y-%m-%d %H:%M:%S")
						
						CSV_FileName = '%s/%s.csv' % (csvFolderPath, attrDict['date'])
						
						# open CSV file
						if (CSV_FileName in csvFileDict):
							outCSVFile = csvFileDict[CSV_FileName]
						else:
							outCSVFile = open(CSV_FileName, 'w')
							outCSVFile.write('latitude,longitude,pm25,timestamp\n')
							csvFileDict[CSV_FileName] = outCSVFile

						outCSVFile.write('%s,%s,%f,%s\n' % (attrDict['gps_lat'], attrDict['gps_lon'], PM25, logDateTime.strftime("%Y/%m/%d %H:%M")))
						dataCounter += 1
						
					except Exception as err:
						print '-',
						errCounter += 1
						if debugLogFile is not None:
							debugLogFile.write('------------------- Error at %d -------------------\n\n%s\n\n%s\n\n\n' % (lineCounter, line, err))
				
				else :
					filteredCounter += 1
					if debugLogFile is not None:
						missing = '';
						
						if PM25 <= 0.0:
							missing = 'PM 2.5, '
							
						if 'gps_lat' not in attrDict or attrDict['gps_lat'] == 0:
							missing = missing + 'gps_lat, '
						
						if 'gps_lon' not in attrDict or attrDict['gps_lon'] == 0:
							missing = missing + 'gps_lon, '
							
						if 'date' not in attrDict:
							missing = missing + 'date, '
							
						if 'time' not in attrDict:
							missing = missing + 'time, '
						
						if 	missing != 'PM 2.5, ' and \
							missing != 'PM 2.5, gps_lat, gps_lon, date, time, ' and \
							missing != 'gps_lat, gps_lon, ' and \
							missing != 'gps_lat, gps_lon, date, time, ':
						
							debugLogFile.write('------------------- Error at %d -------------------\n%s\nMissing Attr: %s\n\n\n' % (lineCounter, line, missing))
				
	elapsedTime  = time.time() - startTime
	
	print''
	print''
	print 'Lines:', lineCounter, ', Data:', dataCounter, ', Err:', errCounter, ', Filtered:', filteredCounter, ', ElapsedTime:', elapsedTime
	print''
	
	if debugLogFile is not None:
		debugLogFile.write('Lines: %d, Data: %d, Err: %d, Filtered: %d, ElapsedTime: %lf\n\n\n\n' % (lineCounter, dataCounter, errCounter, filteredCounter,elapsedTime))
	
	rawlogfile.close()

def main():
	LOG_PATH = '../../data/pm25/logs'
	CSV_PATH = '../../data/pm25/csvs'
	debugLogFile = None
	
	if(len(sys.argv) >= 2 ):
		LOG_PATH = sys.argv[1]
		
	if(len(sys.argv) >= 3) :
		CSV_PATH = sys.argv[2]
		
	if(len(sys.argv) >= 4):
		if sys.argv[3] == '-v':
			DEBUG_LOG_FILENAME = 'preprocessor_log_%s.log' % (time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
			debugLogFile = open(DEBUG_LOG_FILENAME, 'w')
		
	print 'Log path: "%s"' % LOG_PATH
	print 'CSV path: "%s"' % CSV_PATH
	if debugLogFile is not None:
		print 'Debug log file: "%s"' % DEBUG_LOG_FILENAME
	print ''
	
	logFileNames = glob.glob(
		os.path.join(LOG_PATH, "*")
	)
	
	for fileFullName in logFileNames:
		preProcessLogFile(fileFullName, CSV_PATH, debugLogFile)
	
	if debugLogFile is not None:
		debugLogFile.close()
		
if __name__ == "__main__":
	main()
	
	for file in csvFileDict:
		csvFileDict[file].close()