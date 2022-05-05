from pytest import fixture
from logging import basicConfig, getLogger, INFO
from src.mongodb import MongoDb


@fixture
def logger():
    basicConfig(level=INFO)
    return getLogger()


@fixture
def mongo_database():
    database = MongoDb()
    yield database
    database.routines.drop()


@fixture
def mongo_database_one_record(mongo_database):
    mongo_database.insert('routines', {'test_data': 'test_value'})
    test_routines = list(mongo_database.routines.find())
    assert len(test_routines) == 1, 'routines collection size is not equal 1'
    yield mongo_database
