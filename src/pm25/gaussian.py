# -*- coding: utf-8 -*-

from math import radians, cos, sin, asin, sqrt
import numpy as np

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
	print 'km = %f' % km
	return km

def gaussian(x, mu, sig):
	#return (1. / (sig * np.sqrt(2 * np.pi))) * np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
	return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def gaussionLatLon(lat1, lon1, lat2, lon2, radius):
	distance = haversine(lat1, lon1, lat2, lon2)

	if distance > radius:
		return 0
	
	return gaussian(distance, 0, radius / 3.)
	
def main():
	
	print 'weight = %f\n' % (gaussionLatLon(
		24.7870186, 120.9993611,
		24.7870186, 120.9993611,
		20
	))
	
	print 'weight = %f\n' % (gaussionLatLon(
		24.7870186, 120.9993611,
		24.786742, 121.188217,
		20
	))
	
	print 'weight = %f\n' % (gaussionLatLon(
		24.7870186, 120.9993611,
		24.786952, 121.195993,
		20
	))
	
	print 'weight = %f\n' % (gaussionLatLon(
		24.7870186, 120.9993611,
		24.784472, 121.207088,
		20
	))
	
	print 'weight = %f\n' % (gaussionLatLon(
		24.7870186, 120.9993611,
		24.786480, 121.096186,
		20
	))
	
if __name__ == "__main__":
	main()