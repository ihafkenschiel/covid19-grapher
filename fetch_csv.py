
import csv
import requests

CSV_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
OUTPUT_FILE = "data/confirmed_cases.csv"

response = requests.get(CSV_URL)

with open(OUTPUT_FILE, 'w') as f:
    writer = csv.writer(f)
    for line in response.iter_lines():
        writer.writerow(line.decode('utf-8').split(','))
