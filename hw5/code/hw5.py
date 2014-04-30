# Data file:summer season Arctic Sea Ice Extent
# Col 1: year
# Col 2: July
# Col 3: August
# Col 4: September

# Units: square km

# 1. Average the 3 months and differentiate this curve in 5 year intervals. Plot the resulting slope vectors. Use a finite element approach or another way.

# 2. Use a numerical integration technique to compute the total area of the curve from 1870 to 1950 - compare that to the area under the curve from 1950 to 2013

# 3. Smooth the waveform (see http://homework.uoregon.edu/pub/class/355/noise.html) via:
# 	a) boxcar of width 5 years
# 	b) gaussian kernel of width 5 years
# 	c) exponential smoothing with greatest weight given to last 20 years
#    Plot the three waveforms on the same graph and comment on differences in smoothing.

# 4. Plot histogram of yearly ratios of July and Sept sea ice extent, comment on patterns

# 5. Window the data and baseline (polynomial fit ok) to extract two cooling periods prior to 1950 that allow sea extent to remain larger than average. Determine the total area of each event, compare to average area from period 1870 to 1950 to determine overall amplitude of cooling.

# 6. When is meltdown? Use two sets of data:
# 	a) entire data set, determine smooth functional form that best fits data, extrapolate to zero. Do not use polynomial fit in this case. Graph fitted line to the data, extrapolated to zero.
# 	b) use only September satellite data. Fit linear regression to the data, also some power or exponential law. Plot two fits on same graph.

import re
import math
import numpy as np
import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

#split data files into rows
ice = []
with open('../data/icedata.txt','r') as f:
	for line in f:
		s = re.split("\t", line)
		ice.append([int(s[0]),float(s[1]),float(s[2]),float(s[3])])
ice = np.array(ice)

#make a short list to test on
# ice = ice[0:25]
# print ice

# various array slices
# print ice[::5,0] #years by fives
# print ice[0:5,1:] #everything but years in first five years

# sanity check for averaging routine
# for i in range(3):
# 	print np.mean(ice[0:5,i+1])
# print np.mean(ice[0:5,1:]) #average of temps in all 3 months over 5 years

# average the three months
ice_average = []
i = 0
step = 5
while i < len(ice):
	year = ice[i,0]
	area = np.mean(ice[i:i+step,1:])
	ice_average.append([year,area])
	i += step
ice_average = np.array(ice_average)


slope = []
for i in range(len(ice_average)-1):
	slope.append([ice_average[i,0]+step/2,(ice_average[i+1,1]-ice_average[i,1])/step])


plt.figure(0)
plt.plot(ice_average[:,0],ice_average[:,1])
plt.xlabel('Beginning Year of 5 year period')
plt.ylabel('Square kilometers')
plt.title('Average area of arctic ice extent')
plt.savefig('../output/avg_area_five_year')

plt.figure(1)
plt.plot(ice[:,0],(ice[:,1]/ice[:,3]))
plt.xlabel('Year')
plt.title('Ratio of July to September arctic sea ice extent')
plt.savefig('../output/annual_ratio')


