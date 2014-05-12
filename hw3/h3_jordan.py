import re
from collections import Counter

#define a storm object with method for pressure minimum
class storm:

	def __init__(self, id, name, year):
		self.id = id
		self.name = name
		self.pos = []
		self.speed = []
		self.pressure = []
		self.year = year
		self.hr = []
		self.descrip = []

	def pressure_min(self):
		nonzero_pressure = [x for x in self.pressure if x >0]
		if len(nonzero_pressure) == 0:
			return None
		else:
			return min(nonzero_pressure)

	def pressure_max(self):
		return max(self.pressure)


#make a list of storms objects and put in data
storm_list = []
index = 00
i= -1
with open('master1.txt','r') as f:
	for line in f:
		s = re.split("  +", line)
		if index != s[0]:
			new_storm = storm(s[0],s[1],s[6])
			storm_list.append(new_storm)
			i+=1
		index = s[0]
		storm_list[i].pos.append([s[2],s[3]])
		storm_list[i].speed.append(s[4])
		storm_list[i].pressure.append(int(s[5]))
		storm_list[i].hr.append(s[7])
		storm_list[i].descrip.append(s[8])


"""
Checking which storms were actually hurricanes. Turns out all of them became hurricanes.

hurricane_list = [storm for storm in storm_list if any("HURRICANE" in s for s in storm.descrip)]

for storm in hurricane_list:
	print storm.name

print len(storm_list)
print len(hurricane_list)
"""

#count annual frequency
year_list = [int(storm.year) for storm in storm_list]
year_frequency = Counter(year_list)
decade_frequency = Counter()

decade = 1900

for year in year_frequency.elements():
	if year < (decade+10):
		decade_frequency[decade] += 1
	else:
		decade += 10

#check if we counted right:
#x = [storm.name for storm in storm_list if int(storm.year) in range(1980,1990)]
#print len(x)
#missed one when counting...

for decade in decade_frequency: 
	decade_frequency[decade] += 1

print decade_frequency

s = sorted(decade_frequency.items())

bin_width = 10
bins = 13
high = 1010
low = 880
step = (high - low + 0.0) / bins

decade_pressure_dist = []
for i in range(len(s)-2):
	l = [storm for storm in storm_list if s[i+2][0] <= int(storm.year) < (s[i+2][0]+10)]
	a = Counter((float(storm.pressure_min()) - low) // step for storm in l if storm.pressure_min() is not None)
	decade_pressure_dist.append(a)	

out = []

for i in range(9):
	out.append([decade_pressure_dist[i][b] for b in range(bins)])


header = ['Decade']
for i in range(bins):
	bin_low = 880+i*10
	bin_high = bin_low+10
	bin_range = str(bin_low)+"-"+str(bin_high)
	header.append(str(bin_range)+' mbar')

years = ['1920','1930','1940','1950','1960','1970','1980','1990','2000']

with open("hw3_output.txt","w") as output:
	output.write(str(header))
	output.write(",\n")
	for i in range(len(out)):
		google_format = [years[i]]
		for j in range(len(out[i])):
			google_format.append(out[i][j])
		output.write(str(google_format))
		output.write(",\n")




