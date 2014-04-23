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
		# return attributes

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

def filterQuakes(begYear,endYear,begLat,endLat,begLon,endLon,magThresh):
	filtered = [quake.getAll() for quake in quake_list \
	if begYear <= quake.year <= endYear and \
	begLat <= quake.lat <= endLat and \
	begLon <= quake.lon <= endLon and\
	magThresh <= quake.mag
	]

	return filtered

filtered = filterQuakes(1900, 2007, -71.0, 86.7, -180.0, 180.0, 5.5)

print len(filtered), len(quake_list)

with open("../output/hw4_out.txt","w") as output:
	for i in range(len(filtered)):
		output.write(str(filtered[i]))
		output.write(",\n")

