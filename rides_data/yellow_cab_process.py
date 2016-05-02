import csv
from datetime import timedelta, date

filename = 'yellow_tripdata_2015-04.csv'
start_date = '2015-04-07'
end_date = '2015-04-07'
pick_time_start = '18:00:00'
pick_time_end = '19:29:59'


'''six companies' location'''

# GS:
longi_low = -74.016179
longi_high = -74.013117
lati_low = 40.713644
lati_high = 40.715562  

# GOOG:

# longi_low = -74.005104
# longi_high = -74.001477
# lati_low = 40.740372
# lati_high = 40.742359
# Palantir:
# longi_low = -74.006492
# longi_high = -74.005254
# lati_low = 40.739367
# lati_high = 40.740317



def daterange(start_date, end_date):  # set date range
    for n in range(int((end_date - start_date).days)+1):
        yield start_date + timedelta(n)


def main():
    start_year = int(start_date[0:4])
    start_month = int(start_date[5:7])
    start_day = int(start_date[8:10])   # get the year, month, day information of start_date

    end_year = int(end_date[0:4])    # get the year, month, day information of end_date
    end_month = int(end_date[5:7])
    end_day = int(end_date[8:10])

    start_d = date(start_year, start_month, start_day)   # set start date info
    end_d = date(end_year, end_month, end_day)           # set end date info
    range_date = []
    for single_date in daterange(start_d, end_d):
        if single_date.isoweekday() != 6 and single_date.isoweekday() != 7:  # only use weekdays
            range_date.append(single_date.strftime('%Y-%m-%d'))

    f = open('yellow_tripdata_2015-04.csv', "rb")
    rows = csv.reader(f, delimiter=' ', quotechar='|')
    longi_dropoff = []
    lati_dropoff = []
    for i, row_raw in enumerate(rows):
        if i > 0:
            row = row_raw[0].split(",") + row_raw[1].split(",") + row_raw[2].split(",")
            if row[1] == row[3] and row[3] in range_date and pick_time_start <= row[2] and row[2] <= pick_time_end:
                if longi_low <= float(row[7]) and float(row[7]) <= longi_high and lati_low <= float(row[8]) and float(
                        row[8]) <= lati_high:
                    longi_dropoff.append(float(row[11]))
                    lati_dropoff.append(float(row[12]))

    print longi_dropoff
    print lati_dropoff


if __name__ == "__main__":
    main()
