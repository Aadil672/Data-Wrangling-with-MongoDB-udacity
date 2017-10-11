# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)


    data={}
    for i in range(1,9):
        
        colname=sheet.cell_value(0, i)  
        col=sheet.col_values(i, start_rowx=1, end_rowx=sheet.nrows)
        i_max,max_col=col.index(max(col)),max(col)
        
        max_time=sheet.cell_value(i_max+1, 0)
        maxtime=xlrd.xldate_as_tuple(max_time, 0)
        year, month, day, hour, minute, second=maxtime

        data[colname]={'Year': year,
                        'Month': month,
                        'Day': day,
                        'Hour': hour,
                        'maxval': max_col}
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile,delimiter="|")
        writer.writerow(['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'])
        for s in data:
            year = data[s]['Year']
            month = data[s]['Month']
            day = data[s]['Day']
            hour = data[s]['Hour']
            maxLoad = data[s]['maxval']
            writer.writerow([s, year, month, day, hour, maxLoad])

    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()
