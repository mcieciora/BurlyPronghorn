from pytest import fixture
from logging import basicConfig, getLogger, INFO
from src import mongodb


@fixture
def logger():
    basicConfig(level=INFO)
    return getLogger()


@fixture
def mongo_database():
    database = mongodb.MongoDb()
    yield database
    database.main.drop()


@fixture
def mongo_database_one_record(mongo_database):
    mongo_database.insert({'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN',
                           'active_days': '0'})
    yield mongo_database
