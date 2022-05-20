from pytest import fixture
from requests import get


@fixture
def database_with_one_record():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    get('http://0.0.0.0:7999/insert', params=test_data)
    yield
