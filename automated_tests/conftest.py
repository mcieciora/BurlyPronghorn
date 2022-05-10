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
    database.main.drop()


@fixture
def mongo_database_one_record(mongo_database):
    mongo_database.insert({'test_data': 'test_value'})
    test_collection = list(mongo_database.main.find())
    assert len(test_collection) == 1, 'main collection size is not equal 1'
    yield mongo_database
