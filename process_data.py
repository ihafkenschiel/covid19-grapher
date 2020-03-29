
import csv

INPUT_FILE = "data/confirmed_cases.csv"

with open(INPUT_FILE) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    headers = []
    us_data = []
    for row in csv_reader:
        if line_count == 0:
            headers = row
            line_count += 1
        else:
            if row[1] == 'US':
                us_data = row[4:]
                #print(f'\t{row}')
            line_count += 1
    #print(f'Processed {line_count} lines.')

    print(f'{us_data}')
