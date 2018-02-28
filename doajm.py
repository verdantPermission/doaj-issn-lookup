#!/usr/bin/env python3

"""Random information lookup via DOAJ API
USAGE ./doajm.py input_file.csv output_file value_to_search
Ex. python doajm input.csv output.txt apc_url"""

import urllib.request
import urllib.error
import json
import csv
import time
from sys import argv

URL = 'https://doaj.org/api/v1/search/journals/' #URL to API'et
INPUT_FILE = argv[1] #1st. argument containing name of input file.
OUTPUT_FILE = argv[2] #2nd. argument containing name of output file.
SEARCHF = argv[3] #Seatchterm with quotationmarks or without.

def pull_data_api(url):
    """Execute request in API and print either found data or errorcode to terminal."""
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        write_data(OUTPUT_FILE, data)
        print(data)
        time.sleep(0.5)

    except urllib.error.HTTPError as _:
        print(_.reason)

def open_csv():
    """Open file with name INPUT_FILE and calls the function pull_data_api."""
    with open(INPUT_FILE, newline='') as _:
        reader = csv.reader(_, delimiter=';')
        next(_)
        for row in reader:
            pull_data_api(URL + row[0])

def write_data(json_name, data):
    """Write data to file with name OUTPUT_FILE (append mode)."""
    with open(json_name, mode="a") as file:
        try:
            file.write(data['results'][0]['bibjson'][SEARCHF]+'\n')
        except IndexError as _:
            pass

def main():
    """main"""
    open_csv()

if __name__ == '__main__':
    main()
