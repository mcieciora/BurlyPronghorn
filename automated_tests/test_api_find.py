from pytest import mark
from requests import get


@mark.unittest
def test__unit__basic_query(mongo_database_one_record):
    query = {'object_name': 'test_name'}
    return_data = get('http://localhost:7999/find', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    print(return_data.content)
