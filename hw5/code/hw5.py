"""Problem Statements"""
# (DONE) 1. Average the 3 months and differentiate this curve in 5 year intervals. Plot the resulting slope vectors. Use a finite element approach or another way.

# (DONE) 2. Use a numerical integration technique to compute the total area of the curve from 1870 to 1950 - compare that to the area under the curve from 1950 to 2013

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

"""Data Import"""
#split data file into rows (year,July,August,September) - arctic ice sea extent in km^2
ice = []
with open('../data/icedata.txt','r') as f:
	for line in f:
		s = re.split("\t", line)
		ice.append([int(s[0]),float(s[1]),float(s[2]),float(s[3])])
ice = np.array(ice)

# sanity check for averaging routine
# for i in range(3):
# 	print np.mean(ice[0:5,i+1])
# print np.mean(ice[0:5,1:]) #average of temps in all 3 months over 5 years

"""Functions - averages, slopes, integration"""

def get_average(data,step):
	"""Finds average ice extent of 3 months in dataset given year step size"""
	average = []
	i = 0
	while i < len(ice):
		year = ice[i,0]
		area = np.mean(ice[i:i+step,1:])
		average.append([year,area])
		i += step
	average = np.array(average)
	return average

def get_slope(averaged_data):
	"""Finds slope of averaged data."""
	slope =  []
	for i in range(len(averaged_data)-1):
		slope.append([averaged_data[i,0],(averaged_data[i+1,1]-averaged_data[i,1])/5])
		slope.append([averaged_data[i,0]+1,(averaged_data[i+1,1]-averaged_data[i,1])/5])
		slope.append([averaged_data[i,0]+2,(averaged_data[i+1,1]-averaged_data[i,1])/5])
		slope.append([averaged_data[i,0]+3,(averaged_data[i+1,1]-averaged_data[i,1])/5])
		slope.append([averaged_data[i,0]+4,(averaged_data[i+1,1]-averaged_data[i,1])/5])
	slope = np.array(slope)
	return slope

def integrate(start,stop):
	"""Integrates under flat slope curve, starting and stopping on specified years"""
	#value of slope
	i = start - 1870
	integral = 0
	while i < stop - 1870:
		integral += 5*slope[i,1]
		i += 5
	return integral

#one year average
annual_average = get_average(ice,1)

#five year average - excludes 2010-2013 data
ice_average = get_average(ice,5)

#flat line slope, five year average - excludes 2010-2013 data
slope = get_slope(ice_average)

# change of sea ice extent
early = integrate(1870,1950) # 0.166
late = integrate(1950,2009) # 03.055
# print early
# print late

"""Plots"""
plt.figure(0)
plt.plot(ice_average[:,0],ice_average[:,1])
plt.xlabel('Beginning Year of 5 year period')
plt.ylabel('Square kilometers')
plt.title('Area of June-September Arctic sea ice extent, 5 year averages')
plt.savefig('../output/avg_area_five_year')

plt.figure(1)
n, bins, patches = plt.hist(ice[:,1]/ice[:,3],20)
plt.xlabel('Ratio')
plt.ylabel('Number of Events')
plt.title('Histogram of ratio of July to September arctic sea ice extent, all years')
plt.savefig('../output/annual_ratio_hist')

plt.figure(2)
plt.plot(ice[:,0],ice[:,1]/ice[:,3])
plt.xlabel('Year')
plt.ylabel('Ratio')
plt.title('Ratio of July to September arctic sea ice extent, all years')
plt.savefig('../output/annual_ratio')

plt.figure(3)
plt.plot(slope[:,0],slope[:,1])
plt.xlabel('Year')
plt.ylabel('Rate of change, square kilometers/year')
plt.title('Rate of change of area of June-September Arctic sea ice extent, 5 year averages')
plt.savefig('../output/slope')

plt.figure(4)
plt.plot(annual_average[:,0],annual_average[:,1])
plt.xlabel('Year')
plt.ylabel('Square kilometers')
plt.title('Area of June-September Arctic sea ice extent, all years')
plt.savefig('../output/avg_area_annual')





"""crap"""
# plt.figure(4)
# plt.plot(ice_average_all_years[:,0],ice_average_all_years[:,1])

# this didn't do what I thought it would do.
# plt.figure()
# n, bins, patches = plt.hist(ice[:,1]/ice[:,3],20,normed=True)
# plt.xlabel('July:September Ice Extent Ratio')
# plt.ylabel('Probability')
# plt.title('Normalized ratio of July to September arctic sea ice extent')
# plt.savefig('../output/annual_ratio_hist_normed')

