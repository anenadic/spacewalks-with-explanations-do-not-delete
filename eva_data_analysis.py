# https://data.nasa.gov/resource/eva.json (with modifications)
data_f = open('./eva-data.json', 'r', encoding='ascii')
data_t = open('./eva-data-alex.csv', 'w', encoding='utf-8')
g_file = './cumulative_eva_graph.png'

fieldnames = ("EVA #", "Country", "Crew    ", "Vehicle", "Date", "Duration", "Purpose")

data=[]
import json

for i in range(375): # hardcoded number of entries, fragile to changes in the data file
    line=data_f.readline() # read the data file line by line
    print(line)
    data.append(json.loads(line[1:-1])) # ignore the first character on each line (sometimes "[", other times ",") - fragile to the changes in data format
#data.pop(0)
## Comment out this bit if you don't want the spreadsheet
import csv

w=csv.writer(data_t)

import datetime as dt

time = []
date =[]

j=0
for i in data:
    print(data[j])
    # and this bit
    w.writerow(data[j].values()) # writes out each line of data as CSV line
    if 'duration' in data[j].keys():
        tt=data[j]['duration'] #read duration value as string
        if tt == '':
            pass
        else:
            t=dt.datetime.strptime(tt,'%H:%M') #read duration from a string representation into a datetime object
            ttt = dt.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second).total_seconds()/(60*60) # duration converted into (decimal) hours
            print(t,ttt) # print on stdoout the time when the spacewalk started and its duration in decimal hours
            time.append(ttt) # append duration in decimal hours to the time array
            if 'date' in data[j].keys(): # read the date of the spacewalk 
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d')) # read the first characters of the datetime (just the date part) and add to the date list
                #date.append(data[j]['date'][0:10])

            else: # if there is not date value in the data row - ignore that rown and remove the value from the time array too
                time.pop(0)
    j+=1

t=[0] # add 0 as the first value for summing consecutive values
for i in time: # for all spacewalk durations in the time array
    t.append(t[-1]+i) # sum the current duration with the duration in the last element and add that sum as a new element to the array t


date,time = zip(*sorted(zip(date, time))) 
# zip the two arrays together as a tuple ---> res = zip(date, time); print(list(res))
# sorted(zip(date, time)) returns an array sorted by the first argument (date) ---> [(date, time), (date, time), (date, time)]
# zip(*sorted(...)) ---> * operator unpacks an array so each element is a separate argument as zip does not work on a single argument array and needs multiple arguments
# The * in a function call "unpacks" a list (or other iterable), making each of its elements a separate argument
# The * operator is the reverse operation of zipping the data.

import matplotlib.pyplot as plt

plt.plot(date,t[1:], 'ko-') # subset array from the second element till the end t[1:] because the first element is 0 and is an extra array element that is not needed, 'ko-' is the line and dot format of plot function
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(g_file)
plt.show()
