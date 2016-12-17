# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:37:42 2016

@author: Ben
"""

from collections import defaultdict
import MySQLdb
import time
import sys
import json
import unicodecsv as csv

FILE_NAMES = ['C:/Users/Ben/Desktop/power_data/2016-12-14-02_50_01.txt'

              
              
              
              ]

for fileName in FILE_NAMES:
    rawlogfile = open(fileName, "r")
    data=rawlogfile.read().replace('\n', '')
    decodedjson =  json.loads(data)
    D=decodedjson.get("aaData")
    
    count=0
    with open(decodedjson.get("").replace(':', '_') + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PowerType',u"機組名稱",u"裝置容量(千瓩)",u"淨發電量(千瓩)",u"淨發電量/裝置容量比",u"備註"])
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
                
                if powertype !='Pumping Load' and powertype !='Pumping Gen':
                    print powertype+","+name+","+capacity+","+netpowergen+","+percent+","+comment
                    writer.writerow([powertype,name,capacity,netpowergen,percent,comment])
            count+=1
         