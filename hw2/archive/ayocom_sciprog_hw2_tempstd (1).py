# Instructions: use hw2.xls file 
# Column C: Year
# Column D: Temperature in F

# 1. Program: Calculate standard deviation of temperature from arbitrary beginning year and ending year input by user. 

# 2. Calibrate: report standard deviations for the years 1930 to 1960 and 1980 to 2010. 

# 3. Plot: temperature averaged in 10 year increments and standard deviation in 10 year increments. Temp data = red, stddev data = blue.


# Importing the data from .csv, but without the first two columns:

import numpy as np
import scipy as sp
data = np.genfromtxt('hw2.csv', delimiter = ',' , usecols = (2,3))
#print data

# 1. Program: Standard deviation calculation starting/ending at user-defined years in range

# Computes the standard deviation of the temperature given a range of years
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
        
        print "Standard deviation for temperatures in years " + str(begin) \
        + " to " + str(end) + " is " + str(stdev) + " degrees Fahrenheit."
    return stdev


annual_temp_stdev(data,1850,2012)


np.std(data[:,1])


# 2. Calibrate: report standard deviations for the years 1930 to 1960 and 1980 to 2010. 

annual_temp_stdev(data,1930,1960)
annual_temp_stdev(data,1980,2010)


# 3. Plot: temperature averaged in 10 year increments and standard deviation in 10 year increments. Temp data = red, stddev data = blue.


# Less interactive version of annual_temp_stdev, without rounding. How about one for the mean, too.


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


# Now to make data to plot in bins.


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


# Values to sanity check the first bin:


my_mean(data,1850,1860)


my_stdev(data,1850,1860)


plotdata=bin_plot(data,10,1850,2012)


plt.plot(plotdata[0],plotdata[1],'r')


plt.plot(plotdata[0],plotdata[2],'b')



# I still need to figure out how to combine with different vertical axes.... I am new to python and especially matplotlib. 

