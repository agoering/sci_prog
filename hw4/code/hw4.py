# TODO: Produce 5 products from data, as team if want to:
#
# 1. DONE-ish.
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
import math

# define a quake object with following attributes:
# year, lat, long, depth, mag
class quake:

	def __init__(self, year, lat, lon, depth, mag):
		# self.id = id
		self.year = year
		self.lat = lat
		self.lon = lon
		self.depth = depth
		self.mag = mag

	def getAll(self):
		return [self.year,self.lat,self.lon,self.depth,self.mag]
		# return all quake attributes
	
	# Find distance of quake from "origin" point of interest
	# Modified by 'longLatToDist.py' by Wayne Dyck
	def distanceFrom(self, origin):
	    lat1, lon1 = origin
	    lat2, lon2 = self.lat, self.lon
	    # radius = 6378 # km
	    radius = 6378/1.609 #miles

	    dlat = math.radians(lat2-lat1)
	    dlon = math.radians(lon2-lon1)
	    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
	        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	    d = radius * c

	    return d

#make a list of quake objects and put in data
quake_list = []
with open('../data/quake2.txt','r') as f:
	for line in f:
		s = re.split("  +", line)
		new_quake = quake(int(s[0]),float(s[1]),float(s[2]),float(s[3]),float(s[4]))
		quake_list.append(new_quake)

"""
The event counter should be a function that takes input params:
	(beginYear, endYear, begLatitude, endLatitude, begLongitude, endLongitude, 
	 magnitudeThreshold)
	nicknamed (begYear,endYear,begLat,endLat,begLon,endLon,magThresh)
	and returns table (or list of list) of quakes in that time range, 
	in that location range,	above the magnitude threshold. 
	It will help to know the limits of those params also.
"""
#calculate limits
minYear = min(quake.year for quake in quake_list)
maxYear = max(quake.year for quake in quake_list)
minLat = min(quake.lat for quake in quake_list)
maxLat = max(quake.lat for quake in quake_list)
minLon = min(quake.lon for quake in quake_list)
maxLon = max(quake.lon for quake in quake_list)
minMag = min(quake.mag for quake in quake_list)
maxMag = max(quake.mag for quake in quake_list)

with open("../output/var_limits.txt","w") as output:
	output.write(\
		"[minYear,maxYear,minLat,maxLat,minLon,maxLon,minMag,maxMag],\n"
+ str([minYear,maxYear,minLat,maxLat,minLon,maxLon,minMag,maxMag]))

# may want to combine function with user input and output file
def filterQuakes(begYear,endYear,begLat,endLat,begLon,endLon,magThresh):
	filtered = [quake.getAll() for quake in quake_list \
	if begYear <= quake.year <= endYear and \
	begLat <= quake.lat <= endLat and \
	begLon <= quake.lon <= endLon and\
	magThresh <= quake.mag
	]
	return filtered

# output file: call filtered = filterQuakes(...) first
# with open("../output/filter.txt","w") as output:
# for i in range(len(filtered)):
# 	output.write(str(filtered[i]))
# 	output.write(",\n")

# allquakes = filterQuakes(1900, 2007, -71.0, 86.7, -180.0, 180.0, 5.5)
# length of all quakes matches length of quake list. Good.
# print len(allquakes) == len(quake_list)


"""Filtering all the quakes a certain distance from a given point
	seems like a different job than filtering within a range of params.
	So I'm using a different function, which I defined as a method in the
	quake class as distanceFrom.
"""
#taking the lat,long of cities from wherever Google Maps drops the search pin
seattle = (47.7, -122.3)
christchurch = (-43.5,172.6)

def proximityTo(place,miles):
	proximal = [quake.getAll() for quake in quake_list \
	if quake.distanceFrom(place) <= miles]
	return proximal

# I find six quakes within 100 miles of Seattle:
# [[1949, 47.1, -122.392, 30.0, 6.5], [1965, 47.3, -122.333, 65.7, 6.5], 
# [1980, 46.3, -121.994, 15.0, 5.5], [1996, 47.8, -121.745, 8.7, 5.8], 
# [1999, 47.0, -123.234, 48.9, 5.6], [2001, 47.0, -122.58, 54.0, 6.8]]
print proximityTo(seattle,100)




