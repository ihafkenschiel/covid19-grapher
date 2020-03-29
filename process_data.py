
import csv
from datetime import datetime

import numpy as np
from collections import deque,Counter
from bisect import insort, bisect_left
from itertools import islice

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INPUT_FILE = "data/confirmed_cases.csv"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return str(date_obj.month) + '/' + str(date_obj.day)

def RunningMean(seq,M):
    """
     Purpose: Find the mean for the points in a sliding window (fixed size)
              as it is moved from left to right by one point at a time.
      Inputs:
          seq -- list containing items for which a mean (in a sliding window) is
                 to be calculated (N items)
            N -- length of sequence
            M -- number of items in sliding window
      Outputs:
        means -- list of means with size N - M + 1

    """
    N = len(seq)
    # Load deque (d) with first window of seq
    d = deque(seq[0:M])
    means = [np.mean(d)]             # contains mean of first window
    # Now slide the window by one point to the right for each new position (each pass through
    # the loop). Stop when the item in the right end of the deque contains the last item in seq
    for item in islice(seq,M,N):
        old = d.popleft()            # pop oldest from left
        d.append(item)               # push newest in from right
        means.append(np.mean(d))     # mean for current window
    return means

with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    headers = []
    us_data = []
    for row in csv_reader:
        if line_count == 0:
            headers = row[4:]
            headers = map(format_date, headers)
            headers = list(headers)
            line_count += 1
        else:
            if row[1] == 'US':
                us_data = row[4:]
                us_data = list(map(int, us_data)) # cast to int
                #print(f'\t{row}')
            line_count += 1

    print(headers)
    print(us_data)
    print(str(len(headers)) + '/' + str(len(us_data)))

x = headers
y = us_data

ma5 = RunningMean(us_data, 5)
ma5 = [0]*(len(y) - len(ma5)) + ma5 #fill missing beginning values with 0s

ma30 = RunningMean(us_data, 30)
ma30 = [0]*(len(y) - len(ma30)) + ma30 #fill missing beginning values with 0s

fig = plt.figure(figsize=(15,10))
plt.plot(x, y, ma30)
plt.title("US Confirmed Cases of Covid-19")
plt.xlabel('2020')
plt.ylabel('Confirmed Cases')
plt.xticks(x, [str(i) for i in x], rotation=90)

#set parameters for tick labels
plt.tick_params(axis='x', which='major', labelsize=10)
plt.tick_params(axis='y', which='major', labelsize=10)

plt.tight_layout()

plt.savefig('covidcases-US.png')
