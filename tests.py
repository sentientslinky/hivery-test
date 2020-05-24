from people import PeopleAPI
from unittest.mock import MagicMock, patch
from unittest import TestCase
import pytest
from exceptions import InvalidPersonIndexException
from app import port
import requests

class TestIntegration:
    # Test all endpoints to see if they are responding (not 5xx ing)
    @pytest.mark.parametrize("url_fragment", [
        '/paranuara/api/v1.0/people/company_name/20',
        '/paranuara/api/v1.0/people/mutual_living_browneyed_friends/',
        '/paranuara/api/v1.0/people/get_fruits_and_veggies/30'
    ])
    def test_WebAPI(self, url_fragment):
        r = requests.get('http://localhost:{port}{url_fragment}'.format(port=port, url_fragment=url_fragment))
        assert r.status_code < 500
        

class TestUnit(TestCase):
    def test_fruits_and_veggies(self):
        with patch('people.len', return_value=3):
            dbconn_mock = MagicMock()
            cursor = MagicMock()
            cursor.fetchall= MagicMock(return_value=
                [['test', '3', 'orange', 'YES'],
                ['test', '3', 'strawberry', 'YES'],
                ['test', '3', 'pasta', 'NO']])
            dbconn_mock.cursor = MagicMock(return_value=cursor)
            dbconn_mock.cursor().fetch_all()
            
            ret  = PeopleAPI.get_fruits_and_veggies(dbconn_mock, 999)
            print(ret)
            assert ret['name'] == 'test'
            assert 'fruits' in ret.keys()
            assert 'vegetables' in ret.keys()
            assert 'orange' in ret['fruits']
            assert 'pasta' in ret['vegetables']

    def test_fruits_and_veggies_invalid_person(self):
        with patch('people.len', return_value=0):
            dbconn_mock = MagicMock()
            cursor = MagicMock()
            cursor.fetchall= MagicMock(return_value=
                [])
            dbconn_mock.cursor = MagicMock(return_value=cursor)
            dbconn_mock.cursor().fetch_all()
            
            with self.assertRaises(InvalidPersonIndexException):
                PeopleAPI.get_fruits_and_veggies(dbconn_mock, 999)
            