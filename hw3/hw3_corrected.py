# hw3 by Andrea Yocom. 

# master1.txt contents:
# Column 1 is Storm ID
# Column 2 is name of storm
# Column 3,4 is lat/long
# Column 5/6 is wind speed and central pressure
# Column 7 is year
# Column 8 is some running date field in units of hours.
# Column 9 is a descriptor

# TODO: 
# Read/write to paste into Google Code with following format:
# Col 0: Decade, begin 1920 end 2010. String, number, date, datetime ok
# Col 1-n: number of hurricanes in pressure bins: number only

# Syntax required for input to Google Code:
#  # [['Year','min-min+10','min - min+20' ... 'roundup(max)-10 - roundup(max)'],
# [1920,count if in first bin, count if in second bin, ... , count if in last bin],
# ...
# [2010, ...]]
 
# Program determines:
#  - frequency of hurricane events
#  - min(central pressure) for each hurricane event

# 1. (DONE) Isolate hurricanes only
# 2. Isolate distinct storms by decade
# 3. Calculate min central pressure for each distinct storm
# 4. Define pressure bins
# 5. Count frequency of hurricanes, filter by pressure bins

import numpy as np
import scipy as sp

# path to the file to read from
my_file = "master1.txt"
# what to look in each line
look_for = "HURRICANE"
# variable to store relevant data from lines containing specified string
data = []

with open(my_file, "r") as file_to_read:   
    
    for line in file_to_read:
        if look_for in line:
            #eliminate the problem of the space in the name field
            line = line.replace('NOT NAMED','NOT_NAMED')
            #get rid of newline characters
            line = line.strip()
            #split into columns
            columns = line.split()
            
            #the following creates a list of lists
            data.append([int(columns[6]),int(columns[0]),int(columns[5])])


lista=[[1900,371,0],[1900,371,900],[1900,380,0],[1900,380,850],[1901,390,0],[1901,390,890]]

#read each year,id,pressure:
newStorm = [lista[0][0],lista[0][1],lista[0][2]]
distinctStorms = []
for i in range(len(lista)):
    #while in the same year as previous value and same ID as previous value, if not zero, append year,pressure to data
    if lista[i][0] == newStorm[0]:
        if lista[i][1] == newStorm[1]:
            if not lista[i][2] == 0:
                distinctStorms.append([lista[i][0],lista[i][2]])
        #if new storm ID, update newStorm
        else:
            newStorm[1] = lista[i][1]
    #if new year, update newStorm
    else:
        newStorm[0] = lista[i][0]
print pressures


lista=[[1900,371,0],[1900,371,900],[1900,380,0],[1900,380,850],[1901,390,0],[1901,390,890]]

# #split into discrete lists
# years = []
# ids = []
# pressures = []
# for i in range(len(lista)):
#     years.append(lista[i][0])
#     ids.append(lista[i][1])
#     pressures.append(lista[i][2])
    
# print years
# print ids
# print pressures

#print the unique ids

# for i in list(set(ids))

#initialize a list to compare each list within lista against
dummy = [0,0,100000]
keep = []
for i in range(len(lista)):
    
    #loop through unique storms. If new storm, update the keep list with old data, update [year,storm] in dummy, reset dummy pressure
    if lista[i][1] != dummy[1]:
        keep.append(dummy)
        dummy[0] = lista[i][0]
        dummy[1] = lista[i][1]
        dummy[2] = 100000
    #else if we are still on the same storm, we still have to check for lower pressures, but don't update dummy

    if lista[i][2] <= dummy[2]:
        #update pressure in dummy if pressure is a new low
        dummy[2] = lista[i][2]
    #else if we have reached a higher pressure, we loop back to the next row.    
        
    #else if we are still on the same year, we still have to check for unique storms, but no need to update dummy. 
    #therefore year loop is redundant. Included below for reference.
    #loop through unique years row by row
    #if lista[i][0] != dummy[0]:
    #    dummy[0] = lista[i][0]    
print keep

