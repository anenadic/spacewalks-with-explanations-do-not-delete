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
    data.append(json.loads(line[1:-1])) # ignore the first character of each line (sometimes "["", other times ",") - fragile to the format
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
            print(t,ttt) # print time when the spacewalk started and it duration in decimal hours
            time.append(ttt) # append duration in decimal hours to the time array
            if 'date' in data[j].keys(): # read the date of the spacewalk 
                date.append(dt.datetime.strptime(data[j]['date'][0:10], '%Y-%m-%d')) # read the first characters of the datetime (just the date part) and add to the date list
                #date.append(data[j]['date'][0:10])

            else:
                time.pop(0)
    j+=1

t=[0]
for i in time: # for all spacewalk durations in the time array
    t.append(t[-1]+i) # sum the current duration with the duration in the last element and add that sum as a new element to the array t


date,time = zip(*sorted(zip(date, time))) # unzip the sorted tuple array (sorted by the first element of the tuple - i.e. by date)
# The zip() function in Python combines multiple iterables such as lists, tuples, strings, dict etc, into a single iterator of tuples
# names = ['John', 'Alice', 'Bob', 'Lucy']
# scores = [85, 90, 78, 92]
# [('John', 85), ('Alice', 90), ('Bob', 78), ('Lucy', 92)]
# res = zip(names, scores)
# print(list(res))
# The * operator is used to call a function by unpacking an iterable
# We can also reverse the operation by unzipping the data using the * operator.

import matplotlib.pyplot as plt

plt.plot(date,t[1:], 'ko-') # subset array from the second element till the end t[1:] because the first element is 0 and is an extra array element
plt.xlabel('Year')
plt.ylabel('Total time spent in space to date (hours)')
plt.tight_layout()
plt.savefig(g_file)
plt.show()
