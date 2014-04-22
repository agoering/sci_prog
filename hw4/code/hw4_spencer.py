#PHYS 510 Assignment 4

"""
Part 1: Creating list of lists from original data file.

I could have done this in about two lines if I re-saved the file as a csv
before starting, but I hadn't done read a text file directly using Python yet,
so did it this way just to do that.
"""

#Create string dataString from data text file
dataString = open("quake.txt").read()

#stringListBuilder(a string) makes a list where each element is a line
#of that string (i.e., every time a \n is encountered, a new element is made)
#However, the else statement below is made specifically for the data file
#given in this assignment
def stringListBuilder(data):
    data2=[]
    strBuilder=''
    for a in range(0,len(data)):
        if data[a]!='\n':
            strBuilder+=data[a]
        else:
        #One of columns of the data file just has blank spaces for empty data.
        #Replace them with dash marks.
            if strBuilder[8]==' ':
                strBuilder=strBuilder[0:7]+'----'+strBuilder[11:len(strBuilder)]
            data2.append(strBuilder[1:len(strBuilder)])
            strBuilder=''
    return data2

#listListBuilder(a string) makes a list where each element is a list
#which contains the words in a string.
def listListBuilder(data):
    data1=stringListBuilder(data)
    data3=[]
    for a in data1:
        a+=' '
        strBuilder=''
        data2=[]
        for b in a:
            if b !=' ':
                strBuilder+=b
            elif len(strBuilder)!=0:
                data2.append(strBuilder)
                strBuilder=''
        data3.append(data2)
    return data3

#listFormatTest checks whether each element of testList has
#a length of listElementLength
def listFormatTest(testList,listElementLength):
    testBool=True
    for a in testList:
        if len(a)!=listElementLength:
            testBool=False
    return testBool

#dataList is the formatted list containing the raw data given in the
#assignment.
#From this point on, dataList can be treated as the original data
dataList=listListBuilder(dataString)

#Some quick checks to make sure data is formatted correctly
print dataList[0:4]
print dataList[len(dataList)-4:len(dataList)]
print listFormatTest(dataList,7)#Should print True
testInt=0
for a in dataString:
    if a=='\n':
        testInt+=1
print testInt==len(dataList)#Should print True

"""
Part 2: Manipulating the raw data
"""