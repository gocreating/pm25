# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:37:42 2016
@author: Ben
"""

from collections import defaultdict
import glob
import MySQLdb
import time
import sys
import json
import os
import unicodecsv as csv





FILE_NAMES=[]
LOG_PATH = 'C:/Users/Ben/Desktop/power_data'
FILE_NAMES = glob.glob(os.path.join(LOG_PATH, "*.txt"))

with open('temp.csv', 'wb') as csvfile:
    for fileName in FILE_NAMES:
        print(fileName)
        rawlogfile = open(fileName, "r")
        
        data=rawlogfile.read().replace('\n', '')


        decodedjson =  json.loads(data)
        D=decodedjson.get("aaData")
        
        count=0
    
        T=decodedjson.get("").replace('-', '/');
        writer = csv.writer(csvfile)
        #writer.writerow(['PowerType',u"機組名稱",u"裝置容量(千瓩)",u"淨發電量(千瓩)",u"淨發電量/裝置容量比",u"備註"])
        while count<len(D): 
    
            if D[count][1].find(u"小計") ==-1:
                t=D[count][0]
                powertype=t[t.find('(')+1:t.find(')')]
                            
                name=D[count][1]
                name=name.replace("&amp;","&")
                delete=name[name.find('('):name.find(')')+1]
                if delete!='':
                    name=name.replace(delete,"")
                
                         
                capacity=D[count][2]
                if capacity.find('-')!=-1:
                    capacity = "N/A"

                netpowergen=D[count][3]

                percent=D[count][4]
                if percent.find('-')!=-1:
                    if capacity == 'N/A':
                        percent = 'N/A'
                    else:       
                        percent_float= float(netpowergen)*100/float(capacity)
                        if percent_float>100:
                            percent_float=100.0
                        percent=str(percent_float)+'%'
                    
                comment=D[count][5]
                
                if powertype !='Pumping Load' and powertype !='Pumping Gen' and name !=u'汽電共生' and powertype !='Wind' and powertype !='Solar':
                    #print powertype+","+name+","+capacity+","+netpowergen+","+percent+","+T
                    writer.writerow([powertype,name,capacity,netpowergen,percent,T])
            count+=1