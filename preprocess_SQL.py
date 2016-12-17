#-*- coding: utf-8 -*

import MySQLdb

conn = MySQLdb.connect(host="localhost",user="LiYu",passwd="password",db="datamining")
cursor = conn.cursor()

print "Drop table 'rawdata': ",

try:
	cursor.execute("""DROP TABLE `rawdata`""")
	conn.commit()
	print "Success"
	
except Exception as err:
	print "failed"
	print err


print "Create table 'rawdata': ",

try:
	cursor.execute("""CREATE TABLE rawdata (
                    `device_msg`      VARCHAR(255),
                    `ver_format`      TINYINT,
                    `fmt_opt`         TINYINT,
                    `FAKE_GPS`        TINYINT,
                    `app`             VARCHAR(255),
                    `ver_app`         VARCHAR(255),
                    `device_id`       VARCHAR(255),
                    `tick`            BIGINT,
                    `date`            DATE,
                    `time`            TIME,
                    `device`          VARCHAR(255),
                    
                    `s_0`             FLOAT,
                    `s_1`             FLOAT,
                    `s_2`             FLOAT,
                    `s_3`             FLOAT,
                    `s_4`             FLOAT,
                    
                    `s_b0`            FLOAT,
                    `s_b1`            FLOAT,
                    `s_b2`            FLOAT,
					
                    `s_d0`            FLOAT,
                    `s_d1`            FLOAT,
                    `s_d2`            FLOAT,
                    `s_d3`            FLOAT,
                    
                    `s_g0`            FLOAT,
                    `s_g1`            FLOAT,
                    `s_g2`            FLOAT,
                    `s_g3`            FLOAT,
                    `s_g4`            FLOAT,
                    `s_g5`            FLOAT,
                    `s_g6`            FLOAT,
                    `s_g7`            FLOAT,
                    `s_g8`            FLOAT,
                    
                    `s_h0`            FLOAT,
                    `s_h1`            FLOAT,
                    `s_h2`            FLOAT,
                    `s_h3`            FLOAT,
                    `s_h4`            FLOAT,
					`s_h5`            FLOAT,
					
                    `s_l0`            FLOAT,
                    `s_l1`            FLOAT,
                    `s_l2`            FLOAT,
                    `s_l3`            FLOAT,
                    
                    `s_o`             FLOAT,
                    
                    `s_t0`            FLOAT,
                    `s_t1`            FLOAT,
                    `s_t2`            FLOAT,
                    `s_t3`            FLOAT,
					`s_t4`            FLOAT,
					`s_t5`            FLOAT,
                    
                    `s_w0`            FLOAT,
                    `s_w1`            FLOAT,
                    
                    `s_r10`           FLOAT,
                    `s_r60`           FLOAT,
                    
                    `s_s0`             FLOAT,
                    
                    `s_n0`            FLOAT,
                    `s_n1`            FLOAT,
                    
					`s_u0`            FLOAT,
					
                    `t`               FLOAT,
                    `h`               FLOAT,
                    `Humidity`        FLOAT,
                    `Temperature`     FLOAT,
                    
                    `PM10`            FLOAT,
                    `PM2_5`           FLOAT,
                    `PSI`             FLOAT,
                    `FPMI`            FLOAT,
                    `CO`              FLOAT,
                    `NO`              FLOAT,
                    `NO2`             FLOAT,
                    `SO2`             FLOAT,
                    `NOx`             FLOAT,
                    `O3`              FLOAT,
                    `MajorPollutant`  VARCHAR(255),
                    
                    `WindDirec`       FLOAT,
                    `WindSpeed`       FLOAT,
                    
                    `SiteID`          VARCHAR(255),
                    `SiteName`        VARCHAR(255),
                    `SiteEngName`     VARCHAR(255),
                    `SiteType`        VARCHAR(255),
                    `County`          VARCHAR(255),
                    `Status`          VARCHAR(255),
                    
                    `PublishTime`     DATETIME,
                    
                    `gps_lat`         DOUBLE,
                    `gps_lon`         DOUBLE,
                    `gps_fix`         TINYINT,
                    `gps_num`         TINYINT,
                    `gps_alt`         VARCHAR(255)
                    
                    ) """)

	conn.commit()
	print "Success"

except Exception as err:
	print "failed"
	print err

'''
try:
	cursor.execute("SELECT * FROM rawdata")
	results = cursor.fetchall()

	for row in results:
		A = row[0]
		B = row[1]
		C = row[2]
		
		print "A=%s, B=%s, C=%d" % (A, B, C)
	
except:
	print "Error: unable to fecth data"

'''
conn.close()