# TODO: Produce 5 products from data, as team if want to:
#
# 1. 
#   a)Event counter: user enters the following params:
# 	(latitude, longitude, begin year, end year, magnitude threshold)
# 	Counter returns table of values with quakes fitting params
# 	b)Sample output: return earthquakes within 100mile radius from Seattle.
# 2. Clustering detection algorithm:
# 	cluster events at nearly same lat,long,time
# 	output table of clustered events
# 	try to represent clustering visually
# 3. Use D3 Gallery to plot (lat,long) of events within longitude:[-75:-150]
# 4. Use D3 Gallery to make timeline of events > 7.5 magnitude
# 5. Use "happy" multiple axis graph, set up with following for X or Y:
# 	-longitude, depth, magnitude, year
#    See http://d131-92.uoregon.edu/Sandbox/happy/

# Data file ./data/quake.txt contains 6 cols of info sep by 2 spaces.
# Col 1: technique descriptor - extraneous, 
# Col 2: year
# Col 3,4: lat,long
# Col 5: depth under surface; 0 indicates no data
# Col 6: richter scale magnitude of quake

""" Parsing: used csh to do cut -c 13-45 quake.txt > quake2.txt
	to get rid of the technique descriptor
	then all the cols are sep by 2 spaces. Read in to a quake class.
"""

import re
from collections import Counter

# define a quake object with following attributes:
# year, lat, long, depth, mag
class quake:

	def __init__(self, year, lat, long, depth, mag):
		# self.id = id
		self.year = year
		self.lat = lat
		self.long = long
		self.depth = depth
		self.mag = mag

	def getAll(self):
		return [self.year,self.lat,self.long,self.depth,self.mag]
		# return attributes

#make a list of quake objects and put in data
quake_list = []
with open('../data/quake2.txt','r') as f:
	for line in f:
		s = re.split("  +", line)
		new_quake = quake(int(s[0]),float(s[1]),float(s[2]),float(s[3]),float(s[4]))
		quake_list.append(new_quake)

# begYear1 = 2002
# endYear1 = 2008
# print endYear1
# if begYear1 <= quake_list[12874].year and endYear1 >= quake_list[12874].year:
# 	print 'yes'
# else:
# 	print 'no'

# print 'yes' if begYear1 <= quake_list[12874].year <= endYear1 else 'no'

"""
The event counter should be a function that takes input params:
	(minLatitude, maxLatitude, minLongitude, maxLongitude, beginYear, endYear,
	 magnitudeThreshold)
	and returns table (or list of list) of quakes in that time range, 
	in that location range,	above the magnitude threshold.
"""
# print quake_list[0].attributes()
# quake.quakeAttr(quake_list[0])
# def filterQuakes(begYear,endYear):
# 	by_year = [quake for quake in quake_list if begYear <= quake.year <= endYear]

# 	filterResults = by
# filterQuakes(2002,2004)

print quake_list[1].getAll()









