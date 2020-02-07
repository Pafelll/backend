import requests
import os
from requests.exceptions import HTTPError

api_user = os.environ.get('API_USER')
api_pass = os.environ.get('API_PASS')


class Parser:
    def __init__(self):
        self.base_url = 'https://europe-west1-asoc-interview.cloudfunctions.net/get-network-events/'
        self.c_url = self.base_url + '?start='

    @staticmethod
    def get_request(url):
        try:
            response = requests.get(url=url, auth=(api_user, api_pass))
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response

    def fetch_data(self):
        start_id = 1
        url = self.c_url + str(start_id)
        base_set = set()
        while retrieved:= self.get_request(url):
            data = retrieved.text
            if data:
                unique_set, last_record_id = self.find_unique(data)
                base_set.update(unique_set)
                step = int(last_record_id) + 1
                url = self.c_url + str(step)
            else:
                break
        return base_set

    def find_unique(self, data):
        tmp_ = [self.parse_by_split(single_line) for single_line in data.split('\n') if single_line]
        tmp_hashed = [hashed[0] for hashed in tmp_]
        last_record_id = tmp_[-1][1]
        return set(tmp_hashed), last_record_id

    # @stopper
    def parse_by_split(self, data):
        parsed = self.split_and_strip(data)
        if parsed:
            record_id = parsed[0]
            timestamp = self.cut_to_sec(parsed[1])
            source_ip = parsed[2]
            destination_ip = parsed[3]
            payload = parsed[4]
            tmp_set = (timestamp, source_ip, destination_ip, payload)
            return hash(tmp_set), record_id

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
    all_unique_records = p.fetch_data()
    if all_unique_records:
        print(f'Number of unique records: {len(all_unique_records)}')


if __name__ == '__main__':
    main()
