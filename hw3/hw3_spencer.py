from copy import deepcopy
"""
Saved the given Homework 3 file as a csv.
Below, data is a list of lists, corresponding to columns and rows in the csv
"""
import csv
with open("master1.csv") as f:
       r = csv.reader(f)
       data = [row for row in r if row]
"""
I think the assignment indicates that the only type of storm that is of
interest in this assignment are those labelled "HURRICAN". The next line of
code accounts for this, removing all items in data without the label HURRICAN.
To consider other types of storms, simply remove this line of code.
"""
data = [a for a in data if a[9] == 'HURRICAN']

"""
For each item in data data[i],...
    data[i][0] is Storm ID, part 1
    data[i][1] is Storm ID, part 2
    data[i][2] is name of storm
    data[i][3] is latitude
    data[i][4] is longitude
    data[i][5] is wind speed
    data[i][6] is central pressure
    data[i][7] is year
    data[i][8] is running date field in hours
    data[i][9] is a descriptor

To format properly for assignment (i.e., for copying into Google library,
will need to have a list of lists with much of the same information, but
arranged differently. It needs to be...
row 0:
    formattedData[0] is ['Decade', ...central pressure bin ranges as strings...]
row i !=0:
    formattedData[i][0] is decade, e.g., 1920s, as strings
    formattedData[i][j] is totaled number of storms in decade, within
                       binned central pressure range given by
                       formattedData[0][j], as integers
"""

"""
Before making list formattedData, make list tempData, which is the same as data,
but with unecessary columns removed, and with year and central pressure data
binned
"""
tempData=deepcopy(data)

#I think central pressure values of  0 really just stand for "unmeasured".
#Line of code below removes these from tempData
tempData = [a for a in tempData if a[6] != '0']

#For binning and formatting central pressure data, used later
minPress=float(tempData[0][6])
maxPress=float(tempData[0][6])
for a in range(0,len(tempData)):
    if float(tempData[a][6])<minPress:
        minPress=float(tempData[a][6])
    if float(tempData[a][6])>maxPress:
        maxPress=float(tempData[a][6])

divPress=(maxPress-minPress)/6
binPress=[]
for a in range(0,6):
    #Bin into 6 intervals because I'm guessing that's what the assignment
    #wants, since that is the number of country bins in the original Google
    #library file
    binPress.append(minPress+(1+a)*divPress)

#Dictionaries below are for formatting binned data, used later
translator1={1900:'1900s',1910:'1910s',1920:'1920s',1930:'1930s',1940:'1940s',\
1950:'1950s',1960:'1960s',1970:'1970s',1980:'1980s',1990:'1990s',2000:'2000s'}

translator2={binPress[0]:"%.1f - %.1f mbar" %(minPress,(minPress+divPress)),\
binPress[1]:"%.1f - %.1f mbar" %((minPress+divPress),(minPress+2*divPress)),\
binPress[2]:"%.1f - %.1f mbar" %((minPress+2*divPress),(minPress+3*divPress)),\
binPress[3]:"%.1f - %.1f mbar" %((minPress+3*divPress),(minPress+4*divPress)),\
binPress[4]:"%.1f - %.1f mbar" %((minPress+4*divPress),(minPress+5*divPress)),\
binPress[5]:"%.1f - %.1f mbar" %((minPress+5*divPress),(minPress+6*divPress)),\
}

for a in range(0,len(tempData)):
    #Get rid of all entries in tempData except year and central pressure
    tempData[a]=[tempData[a][7],tempData[a][6]]

    #Bin and format year entries
    tempData[a][0]=int(tempData[a][0])-int(tempData[a][0])%10
    tempData[a][0]=translator1[tempData[a][0]]

    #Bin and format central pressure entries
    for b in range(0,len(binPress)):
        if float(tempData[a][1])<=binPress[b]:
            tempData[a][1]=binPress[b]
            break
    tempData[a][1]=translator2[tempData[a][1]]

"""
Onward to the desired formattedData
"""

#Make first row as mentioned above
formattedData=[['Decade']]
for a in range(0,len(binPress)):
    formattedData[0].append(translator2[binPress[a]])

#Make remaining rows
for a in range(0,len(translator1)):
    formattedData.append([translator1[1900+10*a]])
    formattedData[a+1]+=[0]*len(binPress)

#Populate remaing rows
for a in range(1,len(formattedData)):
    for b in range(0,len(tempData)):
        if tempData[b][0]==formattedData[a][0]:
            for c in range(0,len(formattedData[0])-1):
                if tempData[b][1]==formattedData[0][c+1]:
                    formattedData[a][c+1]+=1

#Print out formattedData, nicely formatted for copying onto Google library file
inputString="[\n"
for a in range(0,len(formattedData)):
    inputString=inputString+str(formattedData[a])+",\n"

inputString=inputString[0:len(inputString)-2]+"\n]"

print inputString

"""
That's it for the first part of the assignment. This next part will print
some additional information, but anything printed after inputString should not
be copied into the Google file for creating the chart.

Next part of the assignment:
I am to find "the frequency of Hurricane events". I think this just means the
total number of hurricanes per decade (i.e., report a single number in units of
hurricanes per decade, so I will proceed assuming I interpreted the prompt
correctly. To make sure not to count a given hurrican multiple times, the
relevant piece of information is Storm ID, part 1, which is in data[i][0].

I am also to find "the minimum value of central pressure in each of these
storms". By "storms", I still think that this means, "only hurricanes", so I
will only consider hurricanes. I also think, as above, that values of '0' for
central pressure don't count, so I will ignore these in determining the
minimum value of central pressure for each storm.
"""

tempData=deepcopy(data)
#Make sure tempData is sorted by Storm ID part 1,
#this is assumed in elif statement in for loop below "b=-1" below.
tempData.sort(key=lambda x: int(x[0]))
valuesList=[]
"""
valuesList will be formatted as:
    [...[Hurricane ID part 1, min bin pressure]...].
It will only element for each given Hurricane ID part 1.
"""
for a in range(0,len(tempData)):
    #Get rid of all entries in tempData except Storm ID part 1
    #and central pressure
    tempData[a]=[tempData[a][0],tempData[a][6]]

uniquenessTester=[]
valuesList=[]

#Populate valuesList as described above
b=-1
for a in tempData:
    #populate with a single element for each unique hurricane
    if not a[0] in uniquenessTester:
        uniquenessTester.append(a[0])
        valuesList.append(a)
        b+=1
    #associate with each hurricane its minimum central pressure
    elif valuesList[b][1]=='0' or\
    (int(a[1])<int(valuesList[b][1]) and int(a[1])!=0):
        valuesList[b][1]=a[1]

#We know the storms all took place between 1900 and 2010, i.e., over
#11 decades, so the number of hurricanes per decade is the number of hurricanes
#divided by 11

hurricanesPerDecade=len(valuesList)/float(11)

#We now have and have organized all of the data that we need. The string below
#prints it out in a readable format.

endString="\nThere were %.2f hurricanes per decade between 1900 and 2010.\n\n"\
"The minimum central pressures associated with each hurricane were as "\
"follows:\n"\
%hurricanesPerDecade

for a in valuesList:
    if a[1]!='0':
        endString+="Storm ID: %s    Minimum central pressure: %s mbar\n"\
        %(a[0],a[1])
    else:
        endString+="Storm ID: %s    Minimum central pressure: %s\n"\
        %(a[0],'Unknown')

print endString
