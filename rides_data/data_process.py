import csv

# get data from local csv file
f = open("yellow_tripdata_2015-04.csv", "rb")

# set filter date and time period for further analysis
date = "2015-04-01"
pick_time_start = "18:00:00"
pick_time_end = "18:01:00"

rows = csv.reader(f, delimiter=' ', quotechar='|')
# std output the data into console with certain format
for i, row_raw in enumerate(rows):
    if i > 0:
        row = row_raw[0].split(",") + row_raw[1].split(",") + row_raw[2].split(",")
        # select data which is interested
        if row[1] == row[3] == date and pick_time_start <= row[2] <= pick_time_end:
            print row
