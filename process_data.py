
import csv
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INPUT_FILE = "data/confirmed_cases.csv"

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%m/%d/%y')
    return str(date_obj.month) + '/' + str(date_obj.day)

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
fig = plt.figure(figsize=(15,10))
plt.plot(x, y)
#plt.bar(x, y, alpha=0.2)
plt.title("US Confirmed Cases of Covid-19")
plt.xlabel('2020')
plt.ylabel('Confirmed Cases')
plt.xticks(x, [str(i) for i in x], rotation=90)

#set parameters for tick labels
plt.tick_params(axis='x', which='major', labelsize=10)
plt.tick_params(axis='y', which='major', labelsize=10)

plt.tight_layout()

plt.savefig('covidcases-US.png')
