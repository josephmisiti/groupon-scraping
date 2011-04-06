#!/usr/bin/python

import re

"""

	Quick filtering script to extract data from Groupon's 
	cities pages. Probably a better way to do it but python's 
	re module is 'da bomb'
	
"""


import sys

try: # python 2.6 >
	import set
except:
	from sets import Set

def filter():

	GrouponCities = Set()
	
	lines=open('cities.txt').readlines()
	for line in lines:
		line=line.strip("\r\n")
		city=re.findall(r"href=\"\/([A-Za-z\-]+)\/", line )
		if city and "deals" not in city and "pages" not in city and "merchants" not in city: 
			GrouponCities.add( city[0] )
			
		city=re.findall(r"option value='([A-Za-z:\-]+)'",line)
		if city: 
			if ":" not in city[0]:
				GrouponCities.add(city[0])
			else:
				GrouponCities.add( city[0].split(":")[0] )
				
				
	return GrouponCities
		
if __name__ == "__main__":
	Cities=filter()
	indx=1
	fout=open('Cities.dat','w')
	for City in Cities:
		print "%d %s" %(indx,City)
		fout.write("%s\n" % City )
		indx += 1
	fout.close()