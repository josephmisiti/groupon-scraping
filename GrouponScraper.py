#!/usr/bin/python

"""
	This script will scrape the recent deals section of groupon's site (www.groupon.com/some-city/recent/)
	The following information is currently extracted:
	
		1) city
		2) date of deal
		3) price
		4) total value
		5) savings
		
"""

import os
import sys
import time
import urllib2

from BeautifulSoup import BeautifulSoup


Cities = open('Cities.dat').readlines()

RecentDealsUrl = "http://www.groupon.com/%s/recent/"
RecentDealsUrlAdditionalPages ="http://www.groupon.com/%s/recent?page=%d"

def Scrape(city="",fout=None,indx=0):
	city = city.strip("\n")
	
	for i in range(1,4):
		try:
			if i==1: url = RecentDealsUrl % city
			else: url = RecentDealsUrlAdditionalPages % (city,i)
			
			print "%d trying to scrape: %s" %(indx,url) 
			
			time.sleep(5)
			
			f = urllib2.urlopen(url)
			html=f.read()
			soup = BeautifulSoup(html)
			
			bought = soup.findAll('div', { "class" : "bought" })
			unit_price = soup.findAll('div', { "class" : "price" })
			dates = soup.findAll('p',{"class" : "date"})
			

			if (len(bought) != len(unit_price)) and (len(bought) != len(dates)):
				error()
			
			# price, value, savings
			for i in range(len(bought)):
				NumberPurchased = bought[i].find('span', { "class" : "quantity" }).contents
				prices = unit_price[i].findAll('span', { "class" : "value" })
				Value = [price.contents for price in prices]
				TheDate = dates[i].contents[0].strip('\n').strip()

				print "%s %s %s %s %s %s" % (city, TheDate, NumberPurchased[0], Value[0][0], Value[1][0], Value[2][0])
				fout.write("%s %s %s %s %s %s\n" % (city, TheDate, NumberPurchased[0], Value[0][0], Value[1][0], Value[2][0]))
				
		except (urllib2.HTTPError):
			pass
	
	
if __name__ == "__main__":
	fout=open('PriceData.dat','w')
	indx = 0
	for city in Cities:
		Scrape(city,fout,indx)
		indx += 1
	fout.close()
