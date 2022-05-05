from pytest import mark


@mark.smoke
def test__unit__get_collection_by_name(mongo_database):
    test_data = {
        'routines': mongo_database.routines,
        'tasks': mongo_database.tasks,
        'dreams': mongo_database.dreams
    }
    for test_key, test_value in test_data.items():
        assert mongo_database._get_collection_by_name(test_key) == test_value, \
            'get_collection_by_name returned wrong collection'


@mark.smoke
def test__unit__insert_into_collection(mongo_database):
    mongo_database.insert('routines', {'test_data': 'test_value'})
    test_routines = list(mongo_database.routines.find())
    assert len(test_routines) == 1, 'routines collection size is not equal 1'
    assert test_routines[0]['test_data'] == 'test_value', 'test_data value is not equal to test_value'


@mark.smoke
def test__unit__find_record(mongo_database_one_record):
    test_routines = list(mongo_database_one_record.find('routines', {'test_data': 'test_value'}))
    assert len(test_routines) == 1, 'routines collection size is not equal 1'
    assert test_routines[0]['test_data'] == 'test_value', 'test_data value is not equal to test_value'


@mark.smoke
def test__unit__update_record(mongo_database_one_record):
    mongo_database_one_record.update('routines', {'test_data': 'test_value'}, {'test_data': 'new_value'})
    test_routines = list(mongo_database_one_record.routines.find({}, {'test_data', 'new_value'}))
    assert len(test_routines) == 1, 'routines collection size is not equal 1'
    assert test_routines[0]['test_data'] == 'new_value', 'test_data value is not equal to new_value'


@mark.smoke
def test__unit__delete_record(mongo_database_one_record):
    mongo_database_one_record.delete('routines', {'test_data': 'test_value'})
    test_routines = list(mongo_database_one_record.routines.find())
    assert len(test_routines) == 0, 'routines collection size is not equal 0'
