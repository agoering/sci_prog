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

# Parsing the data file:
# Data file ./data/quake.txt contains 6 cols of info sep by 2 spaces.
# Col 1: technique descriptor - extraneous, 
# Col 2: year
# Col 3,4: lat,long
# Col 5: depth under surface; 0 indicates no data
# Col 6: richter scale magnitude of quake

""" Parsing: used csh to do cut -c 13-45 quake.txt > quake2.txt
	then all the cols are sep by 2 spaces with no extraneous info.
"""

import re
from collections import Counter

# define a quake object with following attributes:
# year, lat, long, depth, mag
class quake:

	def __init__(self, year, lat, lon, depth, mag):
		# self.id = id
		self.year = year
		self.lat = lat
		self.long = lon
		self.depth = depth
		self.mag = mag

#make a list of quake objects and put in data
quake_list = []
with open('../data/quake2.txt','r') as f:
	for line in f:
		s = re.split("  +", line)
		new_quake = quake(s[0],s[1],s[2],s[3],s[4])
		quake_list.append(new_quake)
#make a change
