from pytest import mark


@mark.unit
def test__unit__insert_into_collection(mongo_database):
    mongo_database.insert({'test_data': 'test_value'})
    test_collection = list(mongo_database.main.find())
    assert len(test_collection) == 1, 'main collection size is not equal to 1'
    assert test_collection[0]['test_data'] == 'test_value', 'test_data value is not equal to test_value'


@mark.unit
def test__unit__find_record(mongo_database_one_record):
    test_collection = list(mongo_database_one_record.find({'test_data': 'test_value'}))
    assert len(test_collection) == 1, 'main collection size is not equal to 1'
    assert test_collection[0]['test_data'] == 'test_value', 'test_data value is not equal to test_value'


@mark.unit
def test__unit__update_record(mongo_database_one_record):
    mongo_database_one_record.update({'test_data': 'test_value'}, {'test_data': 'new_value'})
    test_collection = list(mongo_database_one_record.main.find({}, {'test_data', 'new_value'}))
    assert len(test_collection) == 1, 'main collection size is not equal to 1'
    assert test_collection[0]['test_data'] == 'new_value', 'test_data value is not equal to new_value'


@mark.unit
def test__unit__delete_record(mongo_database_one_record):
    mongo_database_one_record.delete({'test_data': 'test_value'})
    test_collection = list(mongo_database_one_record.main.find())
    assert len(test_collection) == 0, 'main collection size is not equal to 0'
