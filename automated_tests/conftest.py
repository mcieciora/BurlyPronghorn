from pytest import fixture
from requests import get
from src.mongodb import MongoDb


@fixture
def empty_mongodb_database():
    database = MongoDb()
    database.db.drop_collection('main')
    yield database


@fixture
def mongodb_database_with_one_record(empty_mongodb_database):
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN'}
    empty_mongodb_database.insert(test_data)
    yield empty_mongodb_database


@fixture
def database_with_one_record_added_by_api_call():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    get('http://0.0.0.0:7999/insert', params=test_data)
    yield
    get('http://0.0.0.0:7999/delete', params={'object_name': 'test_name'})


@fixture
def database_with_one_user_added_by_api_call(empty_mongodb_database):
    test_data = {'username': ['test_user'], 'pass': ['11aa55ee22bb']}
    get('http://0.0.0.0:7999/user_create', params=test_data)
    yield
