"""Problem Statements"""
# (need to make flat slope vectors) 1. Average the 3 months and differentiate this curve in 5 year intervals. Plot the resulting slope vectors. Use a finite element approach or another way.

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

"""Data Manipulations - averages, slopes, integration"""
#one year average
annual_average = []
i = 0
step = 1
while i < len(ice):
	year = ice[i,0]
	area = np.mean(ice[i:i+step,1:])
	annual_average.append([year,area])
	i += step
annual_average = np.array(annual_average)

#five year average
ice_average = []
i = 0
step = 5
while i < len(ice):
	year = ice[i,0]
	area = np.mean(ice[i:i+step,1:])
	ice_average.append([year,area])
	i += step
ice_average = np.array(ice_average)

# print (ice_average)
# print len(ice_average)
#flat line slope, five year average
slope =  []
for i in range(len(ice_average)-1):
	slope.append([ice_average[i,0],(ice_average[i+1,1]-ice_average[i,1])/5])
	slope.append([ice_average[i,0]+1,(ice_average[i+1,1]-ice_average[i,1])/5])
	slope.append([ice_average[i,0]+2,(ice_average[i+1,1]-ice_average[i,1])/5])
	slope.append([ice_average[i,0]+3,(ice_average[i+1,1]-ice_average[i,1])/5])
	slope.append([ice_average[i,0]+4,(ice_average[i+1,1]-ice_average[i,1])/5])
slope = np.array(slope)
print slope


# step = 5
# i = 0
# while i < len(ice_average):
# 	# print ice_average[i,0]
# 	i += 1
# 	years = [l for l in ice[ice_average[i,0]:ice_average[i+5,0],0]]
# 	upper = ice_average(j+5,1)
# 	lower = ice_average(j,1)
# 	slope_value = (upper-lower)/step

#  i in range(len(ice_average)-1):
# 	slope.append([ice_average[i,0]+step/2,(ice_average[i+1,1]-ice_average[i,1])/step])
# slope = np.array(slope)

# puts slope point in middle of year range
# slope = []
# for i in range(len(ice_average)-1):
# 	slope.append([ice_average[i,0]+step/2,(ice_average[i+1,1]-ice_average[i,1])/step])
# slope = np.array(slope)

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

