
import csv
from datetime import datetime

import numpy as np
from collections import deque,Counter
from bisect import insort, bisect_left
from itertools import islice

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

'''
CHANGE COUNTRY HERE
'''
COUNTRIES = ["Brazil", "Costa Rica", "France", "Germany", "Iran", "Israel", "Italy", "Japan", "Mexico", "Philippines", "Russia", "Singapore", "Spain", "Taiwan*", "Turkey", "US"]
print(COUNTRIES)

CASETYPE = input("Confirmed (c) or Deaths (d):")
if CASETYPE == 'd':
    INPUT_FILE = "data/deaths.csv"
    YLABEL = 'Deaths'
else:
    INPUT_FILE = "data/confirmed_cases.csv"
    YLABEL = 'Confirmed Cases'

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
    total_cases = []
    for row in csv_reader:
        if line_count == 0:
            headers = row[4:]
            headers = map(format_date, headers)
            headers = list(headers)
            line_count += 1
        else:
            if row[1] in COUNTRIES:
                COUNTRY = row[1]
                TERRITORY = '' #input("Territory (optional):")

                TERRITORY_STR = '-' + TERRITORY if TERRITORY else ''
                if CASETYPE == 'd':
                    CHART_TITLE = COUNTRY + TERRITORY_STR + " Deaths from Covid-19"
                    IMAGE_FILE = 'images/deaths/coviddeaths-' + COUNTRY + TERRITORY_STR + '.png'
                else:
                    CHART_TITLE = COUNTRY + TERRITORY_STR + " Confirmed Cases of Covid-19"
                    IMAGE_FILE = 'images/confirmed/covidcases-' + COUNTRY + TERRITORY_STR + '.png'

                total_cases = row[4:]
                total_cases = list(map(int, total_cases)) # cast to int
                new_cases = [0] + [y - x for x,y in zip(total_cases,total_cases[1:])]

                print("Country: " + COUNTRY)
                print(headers)
                print("Total Cases: ")
                print(total_cases)
                print("New Cases: ")
                print(new_cases)
                print("Days: " + str(len(headers)) + '/' + str(len(new_cases)))

                x = headers

                ma5 = RunningMean(new_cases, 5)
                ma5 = [0]*(len(new_cases) - len(ma5)) + ma5 #fill missing beginning values with 0s

                ma30 = RunningMean(new_cases, 30)
                ma30 = [0]*(len(new_cases) - len(ma30)) + ma30 #fill missing beginning values with 0s

                fig = plt.figure(figsize=(15,10))
                plt.plot(x, new_cases, label='Cases')
                plt.plot(x, ma5, label='MA5')
                plt.plot(x, ma30, label='MA30')
                plt.title(CHART_TITLE)
                plt.xlabel('2020')
                plt.ylabel(YLABEL)
                plt.xticks(x, [str(i) for i in x], rotation=90)

                #set parameters for tick labels
                plt.tick_params(axis='x', which='major', labelsize=10)
                plt.tick_params(axis='y', which='major', labelsize=10)

                plt.legend()  # Add a legend.
                plt.tight_layout()

                plt.savefig(IMAGE_FILE)

                print("Graph saved in " + IMAGE_FILE)

            line_count += 1
