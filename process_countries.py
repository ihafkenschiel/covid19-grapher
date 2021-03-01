
import csv
from datetime import datetime

import numpy as np
from collections import deque,Counter
from bisect import insort, bisect_left
from itertools import islice

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

'''
CHANGE COUNTRY HERE
'''
COUNTRIES = ["Brazil", "Canada", "Colombia", "Costa Rica", "Ecuador", "France", "Germany", "Iran", "Israel", "Italy", "Japan", "Mexico", "Philippines", "Russia", "Singapore", "Spain", "Sweden", "Taiwan*", "Turkey", "United Kingdom", "US"]
# COUNTRIES = ["Brazil"]
print(COUNTRIES)

CASETYPE = input("Confirmed (c) or Deaths (d):")
if CASETYPE == 'd':
    INPUT_FILE = "data/deaths.csv"
    YLABEL = 'Deaths'
else:
    INPUT_FILE = "data/confirmed_cases.csv"
    YLABEL = 'Confirmed Cases'

def getPopulations():
    """
     Outputs:
        dictionary with country as key and population as value
    """
    populations = {}
    with open("data/population.csv") as myfile:
        for line in myfile:
            country, population = line.partition(",")[::2]
            populations[country.strip()] = int(population)
    return populations


def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return str(date_obj.year) + '/' +str(date_obj.month) + '/' + str(date_obj.day)

def format_months(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return str(date_obj.year) + '/' + str(date_obj.month)

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
    months = []
    total_cases = []
    populations = getPopulations()
    for row in csv_reader:
        if line_count == 0:
            dates = row[4:]
            headers = map(format_date, dates) # y/m/d
            months = map(format_months, dates) # y/m
            headers = list(headers)
            months = list(dict.fromkeys(list(months))) # remove duplicates
            line_count += 1
        else:
            if row[1] in COUNTRIES and row[0] == '':
                COUNTRY = row[1]
                POPULATION = populations[COUNTRY]

                if CASETYPE == 'd':
                    CHART_TITLE = COUNTRY + " Deaths from Covid-19"
                    IMAGE_FILE = 'images/deaths/coviddeaths-' + COUNTRY + '.png'
                else:
                    CHART_TITLE = COUNTRY + " Confirmed Cases of Covid-19"
                    IMAGE_FILE = 'images/confirmed/covidcases-' + COUNTRY + '.png'

                total_cases = row[4:]
                total_cases = list(map(int, total_cases)) # cast to int
                new_cases = [0] + [y - x for x,y in zip(total_cases,total_cases[1:])]

                # Convert to per capita by dividing each case by population
                new_cases = [i/POPULATION for i in new_cases] 
                total_cases = [i/POPULATION for i in total_cases] 

                print("Country: " + COUNTRY)
                print("Population: " + f'{POPULATION:,}')
                # print(headers) # Dates
                # print("Total Cases: ")
                # print(total_cases)
                # print("New Cases: ")
                # print(new_cases)
                print("Days: " + str(len(headers)) + '/' + str(len(new_cases)))

                x = headers

                # ma5 = RunningMean(new_cases, 5)
                # ma5 = [0]*(len(new_cases) - len(ma5)) + ma5 #fill missing beginning values with 0s

                ma14 = RunningMean(new_cases, 14)
                ma14 = [0]*(len(new_cases) - len(ma14)) + ma14 #fill missing beginning values with 0s

                # ma30 = RunningMean(new_cases, 30)
                # ma30 = [0]*(len(new_cases) - len(ma30)) + ma30 #fill missing beginning values with 0s

                fig = plt.figure(figsize=(15,10))
                axes = fig.add_axes([0.1,0.1,0.8,0.8])
                axes.set_ylim([0,0.00001])
                plt.plot(x, new_cases, label='Cases', linewidth=0.5)
                # plt.plot(x, ma5, label='MA5')
                plt.plot(x, ma14, label='MA14', linewidth=1.5)
                # plt.plot(x, ma30, label='MA30')
                plt.title(CHART_TITLE)
                plt.xlabel('Year')
                plt.ylabel(YLABEL)
                
                #set parameters for tick labels
                plt.tick_params(axis='x', which='major', labelsize=10)
                plt.tick_params(axis='y', which='major', labelsize=5)
                plt.xticks(x, [str(i) for i in x], rotation=90)
                for i, tick in enumerate(axes.xaxis.get_ticklabels()):
                    if i % 30 != 0: # skip every 30 days so axis is not so crowded
                        tick.set_visible(False)


                plt.legend()  # Add a legend.
                # plt.tight_layout()

                plt.savefig(IMAGE_FILE)

                print("Graph saved in " + IMAGE_FILE)

                print(" ")

            line_count += 1
