
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INPUT_FILE = "data/confirmed_cases.csv"

with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    headers = []
    us_data = []
    for row in csv_reader:
        if line_count == 0:
            headers = row[4:]
            line_count += 1
        else:
            if row[1] == 'US':
                us_data = row[4:]
                #print(f'\t{row}')
            line_count += 1

    print(headers)
    print(us_data)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(headers,us_data)

fig.savefig('covidcases-US.png')
