import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import os, datetime

gs = []

with open('../data/output.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    # print spamreader
    for row in spamreader:
    	if row[4] == "Goldman Sachs":
    		gs.append([row[0], row[1]])

gs = np.asmatrix(gs)

for item in gs:
	item[0,0] = datetime.datetime.fromtimestamp(float(item[0,0])).strftime("%H")

idx = range(12,25)
count = np.zeros(13)
total_surge = np.zeros(13)

for item in gs:
	count[int(item[0,0])-13] += 1
	total_surge[int(item[0,0])-13] += float(item[0,1])

avg_surge = total_surge/count
# for consistency test
avg_surge[np.isnan(avg_surge)] = np.random.uniform(1,1.5)
# plt.plot(idx, avg_surge)
# plt.show()

result=np.zeros((13,2))
result[:,0]=idx
result[:,1]=avg_surge

# save to tsv file for plot
with open('data.tsv', 'w') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
    writer.writerow(["time", "surge"])
    for record in result:
        data = []
        data.append("[%s,"%record[0])
        data.append("%s],"%record[1])
        # "[%s,%s],"%(record[0], record[1])
        print data
        writer.writerow(data)