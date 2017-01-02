# -*- coding: utf-8 -*-

import numpy as np
import random
	
def main():
	a = np.zeros((6,5))
	b = np.random.rand(6,5)
	c = np.random.rand(6,5)
	
	print a
	print b
	print
	
	for i in range(0, 1000):
		r = random.randint(0,5)
		c = random.randint(0,4)
		a[r][c] = a[r][c] + 1
		
	print a
	print b / a
	
if __name__ == "__main__":
	main()