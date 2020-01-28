import pytest
from main import Parser
import requests


@pytest.fixture(params=['test_data1_all.txt', 'test_data2_all.txt', 'test_data3_all.txt'])
def read_all_unique(request):
    with open(request.param, 'r+') as f:
        data = f.read()
        return data


@pytest.fixture()
def read_2_unique():
    with open('test_data1_2unique.txt', 'r+') as f:
        data = f.read()
        return data


@pytest.fixture()
def read_3_unique():
    with open('test_data2_3unique.txt', 'r+') as f:
        data = f.read()
        return data


@pytest.fixture()
def parser():
    return Parser()


def test_cut_to_sec(parser):
    assert parser.cut_to_sec('2019-09-01T00:00:00.04Z') == '2019-09-01T00:00:00'
    assert parser.cut_to_sec('2019-09-01T00:00:00.04Z.324') == '2019-09-01T00:00:00'
    assert parser.cut_to_sec('2019-09-01T0.0:00:00.04Z.324') != '2019-09-01T00:00:00'


def test_parse_by_split(parser):
    assert parser.parse_by_split('15 2019-09-01T00:00:00.15Z 10.12.117.145 209.22.11.160 YfgYtgdPV+IruZwDVrj5Tg') == (
        '2019-09-01T00:00:00', '10.12.117.145', '209.22.11.160', 'YfgYtgdPV+IruZwDVrj5Tg')
    assert parser.parse_by_split('  id    2019-09-01T00:00:00.13Z tyu     yui   ip') == (
        '2019-09-01T00:00:00', 'tyu', 'yui', 'ip')
    assert parser.parse_by_split('  id    23.tdtdtdf tyu     yui   ip') == ('23', 'tyu', 'yui', 'ip')


def test_find_unique(parser, read_all_unique):
    n_unique, n_total = parser.find_unique(read_all_unique)
    assert (len(n_unique), n_total) == (8, 8)


def test_find_unique2(parser, read_2_unique):
    n_unique, n_total = parser.find_unique(read_2_unique)
    assert (len(n_unique), n_total) == (1, 6)


def test_find_unique3(parser, read_3_unique):
    n_unique, n_total = parser.find_unique(read_3_unique)
    assert (len(n_unique), n_total) == (2, 6)


def test_get_request(parser):
    url = 'https://europe-west1-asoc-interview.cloudfunctions.net/get-network-events/?start=1000'
    assert parser.get_request(url).status_code == requests.codes.ok


def test_fetch_data(parser):
    resp = parser.fetch_data()
    assert len(resp) > 0

