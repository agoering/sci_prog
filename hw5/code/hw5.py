"""Problem Statements"""
# (DONE) 1. Average the 3 months and differentiate this curve in 5 year intervals. Plot the resulting slope vectors. Use a finite element approach or another way.

# (DONE) 2. Use a numerical integration technique to compute the total area of the curve from 1870 to 1950 - compare that to the area under the curve from 1950 to 2013

# 3. Smooth the waveform (see http://homework.uoregon.edu/pub/class/355/noise.html) via:
#   a) boxcar of width 5 years
#   b) gaussian kernel of width 5 years
#   c) exponential smoothing with greatest weight given to last 20 years
#    Plot the three waveforms on the same graph and comment on differences in smoothing.

# 4. Plot histogram of yearly ratios of July and Sept sea ice extent, comment on patterns

# 5. Window the data and baseline (polynomial fit ok) to extract two cooling periods prior to 1950 that allow sea extent to remain larger than average. Determine the total area of each event, compare to average area from period 1870 to 1950 to determine overall amplitude of cooling.

# 6. When is meltdown? Use two sets of data:
#   a) entire data set, determine smooth functional form that best fits data, extrapolate to zero. Do not use polynomial fit in this case. Graph fitted line to the data, extrapolated to zero.
#   b) use only September satellite data. Fit linear regression to the data, also some power or exponential law. Plot two fits on same graph.

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
#   print np.mean(ice[0:5,i+1])
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

"""Functions: Smoothing algorithms borrowed from Gene"""
## The following algorithm smoothes data using n-point sliding box-car 
## smoothing. Stolen from http://users.aims.ac.za/~mike/python/env_modelling.html
## this is a better algorithm because it takes care of the "residuals" by 
## reflecting the data around the endpoints

def smootherBox(x, n):
     x_smooth = []
     L = len(x)
     store = np.zeros((n,1), float)  ## array of zeroes for each group of 
     for u in range(0, L-n):      ## used to produce smoothed value
          for v in range(0, n):  ##  add the values and divide by their number
               store[v] = x[u+v]
          av = float(sum(store)) / n  ## repeat for each value at center
          x_smooth.append(av)
     for u in range(L-n,L):  ## this takes care of the "residual" at the end
          for v in range(0, L-u-1):  ## average the values and find the smoothed value
               store[v] = x[u+v]
          av = float(sum(store)) / n
          x_smooth.append(av)
     return x_smooth

def smootherGauss(x, n):
     coeff = [0.067, 0.242, 0.383, 0.242, 0.067]
## these are coefficients corresponding to Gaussian kernel of width 5
## taken from the web page homepages.inf.ed.ac.uk/rbf/HIPR2/gsmooth.htm
     x_smooth = []
     L = len(x)
     store = np.zeros((n,1), float)  ## array of zeroes for each group of 
     for u in range(0, L-n):      ## used to produce smoothed value
          for v in range(0, n):   ##  add the values multiplied by gaussian coefficients
               store[v] = x[u+v]
          av = 0
          for i in range(0, len(coeff)):
               av += float(coeff[i]) * float(store[i])
          x_smooth.append(av)
     for u in range(L-n,L):  ## this takes care of the "residuals" at the end
          for v in range(0, L-u-1):  ## average the values and find the smoothed value
               store[v] = x[u+v]
          av = 0
          for i in range(0, len(coeff)):
               av += float(coeff[i]*store[i])
          x_smooth.append(av)
     return x_smooth

## in exponential smoothing each value is defined as
## s[0] = x[0] and s[t] = a x[t-1] + (1-a) s[t-1]
## where 0<a<1 is smoothing parameter.  Larger values of a
## give more weight to recent data but smoothing is worse
def smootherExp(x, a):
    x_smooth = []
    L = len(x)
    x_smooth.append(x[0])
    for u in range(1, L):
        store = a * float(x[u-1]) + (1-a) * float(x_smooth[u-1])
        x_smooth.append(store)
    return x_smooth

"""Calculations and data preparation for plots"""    
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

#smoothed ice extent data
box_smooth_list = smootherBox(annual_average[:,1],5)
box_smooth = np.array([[annual_average[i,0],box_smooth_list[i]] for i in range(len(box_smooth_list))])

gauss_smooth_list = smootherGauss(annual_average[:,1],5)
gauss_smooth = np.array([[annual_average[i,0],gauss_smooth_list[i]] for i in range(len(gauss_smooth_list))])

exp_smooth_all = []
for i in np.arange(0,1,0.1):
    exp_smooth_list = smootherExp(annual_average[:,1],i)
    exp_smooth = np.array([[annual_average[i,0],exp_smooth_list[i]] for i in range(len(exp_smooth_list))])
    exp_smooth_all.append(exp_smooth)

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

plt.figure(5)
plt.plot(annual_average[:,0],annual_average[:,1],label=r'raw data', color='black')
plt.plot(box_smooth[:,0],box_smooth[:,1],label=r'boxcar-smoothed data', color='blue')
plt.plot(gauss_smooth[:,0],gauss_smooth[:,1],label=r'Gaussian-smoothed data', color='green')
plt.plot(exp_smooth_all[7][:,0], exp_smooth_all[7][:,1],label=r'exponential-smoothed data, smoothing parameter 0.7',color='red')
plt.xlabel('Year')
plt.ylabel('Square kilometers')
plt.title('Smoothed Area of June-September Arctic sea ice extent, all years')
plt.legend(loc='lower left')
leg = plt.gca().get_legend()
ltext  = leg.get_texts()
plt.setp(ltext, fontsize='small') 
plt.savefig('../output/smooth_avg_area_annual')

# generate exponentially smoothed plot commands
# for i in range(10):
#     j = np.arange(0,1,0.1)[i]
#     print 'plt.plot(exp_smooth_all['+str(i)+'][:,0], exp_smooth_all['+str(i)+'][:,1],label=r\'exponential-smoothed data, smoothing parameter '+str(j)+'\')'

plt.figure(6)
plt.plot(exp_smooth_all[1][:,0], exp_smooth_all[1][:,1],label=r'exponential-smoothed data, smoothing parameter 0.1')
plt.plot(exp_smooth_all[2][:,0], exp_smooth_all[2][:,1],label=r'exponential-smoothed data, smoothing parameter 0.2')
plt.plot(exp_smooth_all[3][:,0], exp_smooth_all[3][:,1],label=r'exponential-smoothed data, smoothing parameter 0.3')
plt.xlabel('Year')
plt.ylabel('Square kilometers')
plt.title('Various Exponentially Smoothed Ice Extent Averages')
plt.legend(loc='lower left')
plt.savefig('../output/expsmooth123')

plt.figure(7)
plt.plot(exp_smooth_all[4][:,0], exp_smooth_all[4][:,1],label=r'exponential-smoothed data, smoothing parameter 0.4')
plt.plot(exp_smooth_all[5][:,0], exp_smooth_all[5][:,1],label=r'exponential-smoothed data, smoothing parameter 0.5')
plt.plot(exp_smooth_all[6][:,0], exp_smooth_all[6][:,1],label=r'exponential-smoothed data, smoothing parameter 0.6')
plt.xlabel('Year')
plt.ylabel('Square kilometers')
plt.title('Various Exponentially Smoothed Ice Extent Averages')
plt.legend(loc='lower left')
plt.savefig('../output/expsmooth456')

plt.figure(8)
plt.plot(exp_smooth_all[7][:,0], exp_smooth_all[7][:,1],label=r'exponential-smoothed data, smoothing parameter 0.7')
plt.plot(exp_smooth_all[8][:,0], exp_smooth_all[8][:,1],label=r'exponential-smoothed data, smoothing parameter 0.8')
plt.plot(exp_smooth_all[9][:,0], exp_smooth_all[9][:,1],label=r'exponential-smoothed data, smoothing parameter 0.9')
plt.xlabel('Year')
plt.ylabel('Square kilometers')
plt.title('Various Exponentially Smoothed Ice Extent Averages')
plt.legend(loc='lower left')
plt.savefig('../output/expsmooth789')





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

