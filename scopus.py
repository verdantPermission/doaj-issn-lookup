#!/usr/bin/env python3

"""Random information lookup via SCOPUS API
USAGE ./scopus.py input_file.csv output_file
Ex. python scopus input.csv output.txt"""

import urllib.request
import urllib.error
import json
import csv
import time
from sys import argv

URL = 'https://api.elsevier.com/content/serial/title/issn/' #URL to API'et
INPUT_FILE = argv[1] #1st. argument containing name of input file.
OUTPUT_FILE = argv[2] #2nd. argument containing name of output file.
API_KEY= '*** YOUR API KEY GOES HERE ***'

def pull_data_api(issn):
    """Execute request in API and print either found data or errorcode to terminal."""
    url = URL + issn.replace('-', '') + '?apiKey=' + API_KEY
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        jsonString = response.read()
        print(jsonString)
        jsonResult = json.loads(jsonString)
        write_data(OUTPUT_FILE, issn, jsonResult)

    except urllib.error.HTTPError as _:
        print(_.reason)
        write_data(OUTPUT_FILE, issn, None)

def open_csv():
    """Open file with name INPUT_FILE and calls the function pull_data_api."""
    with open(INPUT_FILE, newline='') as _:
        reader = csv.reader(_, delimiter=',')
        for row in reader:
            print(row)
            pull_data_api(row[0])

def write_data(output_filename, issn, data):
    """Write data to file with name OUTPUT_FILE (append mode)."""
    with open(output_filename, mode="a") as file:
        try:
            file.write(issn + ',')
            if (data != None) :
                file.write(data['serial-metadata-response']['entry'][0]['dc:title'])
        except IndexError as _:
            pass
        file.write('\n')

def main():
    """main"""
    open_csv()

if __name__ == '__main__':
    main()
