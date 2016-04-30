import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import os, datetime

def companyDate(name, day):
    # save time with urge_multiplier into tsv file
    gs = []

    with open('../data/output.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        # print spamreader
        for row in spamreader:
        	if row[4] == name and datetime.datetime.fromtimestamp(float(row[0])).strftime("%d") in day:
        		gs.append([row[0], row[1]])

    gs = np.asmatrix(gs)

    for item in gs:
    	item[0,0] = datetime.datetime.fromtimestamp(float(item[0,0])).strftime("%H")

    idx = range(1,25) # 1:24
    count = np.zeros(24)
    total_surge = np.zeros(24)

    for item in gs:
    	count[int(item[0,0])] += 1
    	total_surge[int(item[0,0])] += float(item[0,1])

    avg_surge = total_surge/count
    # for consistency test by imputing data with reasonable random number
    avg_surge = [np.random.uniform(1, 1.5) if np.isnan(x) else x for x in avg_surge]

    result=np.zeros((24,2))
    result[:,0]=idx
    result[:,1]=avg_surge

    # save to tsv file for plot
    with open('data.tsv', 'w') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t', lineterminator='\n')
        writer.writerow(["time", "surge", "company", "start", "end"])
        for record in result:
            # data = []
            if record[0]>= 12:
                # data.append("[%s,"%record[0])
                # data.append("%s],"%record[1])
                writer.writerow([record[0], record[1], name, int(day[0]), int(day[-1])])

if __name__ == '__main__':
    # 1)
    # companyDate("Goldman Sachs", ["26"])
    # companyDate("Deutsche Bank", ["26"])
    # companyDate("Google", ["26"])
    # companyDate("Palantir", ["26"])
    # companyDate("Bloomberg", ["26"])
    # companyDate("WSJ", ["26"])
    # 2)
    # companyDate("Goldman Sachs", ["22","29"])
    # companyDate("Deutsche Bank", ["22","29"])
    # companyDate("Google", ["22","29"])
    # companyDate("Palantir", ["22","29"])
    # companyDate("Bloomberg", ["22","29"])
    # companyDate("WSJ", ["22","29"])
    # 3)
    # companyDate("Goldman Sachs", ["18","19","20","21","25","26","27","28"])
    # companyDate("Deutsche Bank", ["18","19","20","21","25","26","27","28"])
    # companyDate("Google", ["18","19","20","21","25","26","27","28"])
    # companyDate("Palantir", ["18","19","20","21","25","26","27","28"])
    # companyDate("Bloomberg", ["18","19","20","21","25","26","27","28"])
    companyDate("WSJ", ["18","19","20","21","25","26","27","28"])