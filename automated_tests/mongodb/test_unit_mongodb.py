from pytest import mark


@mark.unittests
def test__unit__insert_one_record(empty_mongodb_database):
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN'}
    return_status = empty_mongodb_database.insert(test_data)
    assert return_status is True, f'Incorrect return_status value: {return_status}'
    return_data = list(empty_mongodb_database.db['main'].find())
    assert len(return_data) == 1, f'Incorrect return data length: {return_data}'
    assert return_data[0]['object_name'] == 'test_name', f"Incorrect object_name value: {return_data[0]['object_name']}"
    assert return_data[0]['note'] == 'example_note', f"Incorrect note value: {return_data[0]['note']}"
    assert return_data[0]['related_tasks'] == 'NaN', f"Incorrect related_tasks value: {return_data[0]['related_tasks']}"


@mark.unittests
def test__unit__insert_same_record_two_times(mongodb_database_with_one_record):
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN'}
    return_status = mongodb_database_with_one_record.insert(test_data)
    assert return_status is False, f'Incorrect return_status value: {return_status}'
    return_data = list(mongodb_database_with_one_record.db['main'].find())
    assert len(return_data) == 1, f'Incorrect return data length: {return_data}'


@mark.unittests
def test__unit__find_one_record(mongodb_database_with_one_record):
    return_data = list(mongodb_database_with_one_record.find({'object_name': 'test_name'}))
    assert len(return_data) == 1, f'Incorrect return data length: {return_data}'


@mark.unittests
def test__unit__delete_one_record(mongodb_database_with_one_record):
    return_value = mongodb_database_with_one_record.delete({'object_name': 'test_name'})
    assert return_value is True, f'Incorrect return data value: {return_value}'
    return_data = list(mongodb_database_with_one_record.db['main'].find())
    assert len(return_data) == 0, f'Incorrect return data length: {return_data}'


@mark.unittests
def test__unit__delete_nonexistent_record_empty_database(empty_mongodb_database):
    return_value = empty_mongodb_database.delete({'object_name': 'test_name'})
    assert return_value is False, f'Incorrect return data value: {return_value}'
    return_data = list(empty_mongodb_database.db['main'].find())
    assert len(return_data) == 0, f'Incorrect return data length: {return_data}'


@mark.unittests
def test__unit__delete_nonexistent_record(mongodb_database_with_one_record):
    mongodb_database_with_one_record.delete({'object_name': 'no_name'})
    return_data = list(mongodb_database_with_one_record.db['main'].find())
    assert len(return_data) == 1, f'Incorrect return data length: {return_data}'
