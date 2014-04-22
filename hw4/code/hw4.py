# TODO: Produce 5 products from data, as team if want to:
#
# 1. Event counter: user enters the following
# 	(latitude, longitude, begin year, end year, magnitude threshold)
# 	Counter returns values
# 	No GUI interface needed
# 	Sample output: earthquake occurrences within radius of 100miles
# 			from Seattle.
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

# Strategy: use a class to wrap this data.

import re
from collections import Counter

# define a quake object with attributes:
# year, lat, long, depth, mag
class quake:

	def __init__(self, year, lat, long, depth, mag):
		self.id = id
		self.lat = []
		self.long = []
		self.beg = []
		self.end = []
		self.mag = []

	def pressure_min(self):
		nonzero_pressure = [x for x in self.pressure if x >0]
		if len(nonzero_pressure) == 0:
			return None
		else:
			return min(nonzero_pressure)

	def pressure_max(self):
		return max(self.pressure)
