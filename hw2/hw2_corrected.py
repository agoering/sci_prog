#TODO:

# Contents of hw2.csv:
# Column C: Year
# Column D: Temperature in F

# 1. (DONE) Program: Calculate standard deviation of temperature from arbitrary beginning year and ending year input by user. 

# 2. (DONE - see calibration.txt) Calibrate: report standard deviations for the years 1930 to 1960 and 1980 to 2010. 

# 3. (DONE - see temp_plot.ps) Plot: temperature averaged in 10 year increments and standard deviation in 10 year increments. Temp data = red, stddev data = blue.

import numpy as np
import scipy as sp
data = np.genfromtxt('./data/hw2.csv', delimiter = ',' , usecols = (2,3))
#print data

import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

# Verbose function to return the standard deviation of the temperature given a range of years
def annual_temp_stdev(data,begin,end):
    """data must be a 2-col array of year and temp, begin and end are years to define averaging"""
    #check to make sure begin and end are within range
    if begin not in data[:,0]:
        print "Beginning year not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    elif end not in data[:,0]:
        print "Ending year not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    else:
        #index the begin and end years
        ibegin = begin - data[0,0]
        iend = end - data[0,0]
        
        #compute standard deviation of the temperatures in the range indicated by years
        stdev = np.std(data[ibegin:iend+1,1])
        #round
        stdev = round(stdev,3)
        
        return "Standard deviation for temperatures in years " + str(begin) \
        + " to " + str(end) + " is " + str(stdev) + " degrees Fahrenheit."
    # return stdev

# Computes the standard deviation of the 2nd col given a range of items in the 1st col
def my_stdev(data,begin,end):
    """data must be a 2-col array, begin and end are endpoints to define averaging"""
    #check to make sure begin and end are within range
    if begin not in data[:,0]:
        print "begin not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    elif end not in data[:,0]:
        print "end not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    else:
        #index the begin and end points
        ibegin = begin - data[0,0]
        iend = end - data[0,0]
        
        #compute standard deviation of the data in the range indicated by [begin:end+1]
        stdev = np.std(data[ibegin:iend+1,1])
    return stdev


# Computes the mean of the 2nd col given a range of items in the 1st col
def my_mean(data,begin,end):
    """data must be a 2-col array, begin and end are endpoints to define averaging"""
    #check to make sure begin and end are within range
    if begin not in data[:,0]:
        print "begin not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    elif end not in data[:,0]:
        print "end not in range " + str(data[0,0]) + " to " + str(data[len(data)-1,0]) + ", try again."
    else:
        #index the begin and end points
        ibegin = begin - data[0,0]
        iend = end - data[0,0]
        
        #compute standard deviation of the data in the range indicated by [begin:end+1]
        datamean = np.mean(data[ibegin:iend+1,1])
    return datamean

def bin_plot(data,binsize,begin,end):
    #initialize lists to store binned averages and stdevs
    years = []
    means = []
    stdevs = []
    
    #loop in increments of binsize to populate lists, up to the last full decade (doesn't work for 2011,2012 in this vsn)
    i = 0
    while i < int(round(2012-1850,-1)):
        years.append(begin+i)
        means.append(my_mean(data,begin+i,begin+i+binsize))
        stdevs.append(my_stdev(data,begin+i,begin+i+binsize))
        i += binsize
    return [years,means,stdevs]

plotdata=bin_plot(data,10,1850,2012)

[years,means,stdevs] = plotdata

#Calibrate: report standard deviations for the years 1930 to 1960 and 1980 to 2010. 

thirtyToSixty = annual_temp_stdev(data,1930,1960)
eightyToTen = annual_temp_stdev(data,1980,2010)
#output calibration
with open('./ch/calibration.txt','w') as f:
    # printString =
    f.write(thirtyToSixty + ' ' + eightyToTen)


#plotting code borrowed from Jordan
plt.plot(years,means,'ro')
plt.errorbar(years,means,yerr=stdevs,linestyle = 'None',color='blue')
plt.xlabel('Decade')
plt.ylabel("Average Temperature")
plt.title("Average Temperature by Decade")
plt.xlim([1840,2012])
plt.ylim([57,60])
plt.savefig('./img/temp_plot')