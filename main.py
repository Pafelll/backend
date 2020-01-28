import requests
import os
import json
from collections import namedtuple

api_user = os.environ.get('API_USER')
api_pass = os.environ.get('API_PASS')


class Parser:
    def __init__(self):
        self.base_url = 'https://europe-west1-asoc-interview.cloudfunctions.net/get-network-events/'
        self.c_url = self.base_url + '?start='

    @staticmethod
    def get_request(url):
        return requests.get(url=url, auth=(api_user, api_pass))

    def fetch_data(self):
        step = 1
        url = self.c_url
        fetched_data = ''
        while retrieved:= self.get_request(url):
            data = retrieved.text
            if data:
                fetched_data += data
            else:
                break
            step += 1000
            url = self.c_url + str(step)
        return fetched_data

    def find_unique(self, data):
        base_set = set()
        tmp_ = [self.parse_by_split(single_line) for single_line in data.split('\n') if single_line]
        total_amount = len(tmp_)
        base_set.update(tmp_)
        return base_set, total_amount

    # @stopper
    def parse_by_split(self, data):
        parsed = self.split_and_strip(data)
        # Records = namedtuple('Records', 'id timestamp source_ip destination_ip payload')
        if parsed:
            timestamp = self.cut_to_sec(parsed[1])
            source_ip = parsed[2]
            destination_ip = parsed[3]
            payload = parsed[4]
            tmp_set = (timestamp, source_ip, destination_ip, payload)
            return tmp_set

    @staticmethod
    def cut_to_sec(timestamp):
        return timestamp.split('.')[0][:19]  # [:19] cut zone in some cases

    @staticmethod
    def split_and_strip(data):
        return [value.strip() for value in data.split(' ') if value]

    @staticmethod
    def save_file_txt(data, file_name='datas.txt'):
        with open(file_name, 'w') as f:
            f.write(data)


def main():
    print('Initialize program...')
    p = Parser()
    print('Fetching data from api...')
    all_records = p.fetch_data()
    print('Finding unique records...')
    unique_records, total_records = p.find_unique(all_records)
    print(f'Total amount of records: {total_records}')
    print(f'Number of unique records: {len(unique_records)}')


if __name__ == '__main__':
    main()
