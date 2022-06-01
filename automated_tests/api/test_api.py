from pytest import mark
from requests import get


@mark.regression
def test__regression__insert_too_short_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_too_long_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0',
                 'additional_key': 'value'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_wrong_keys_in_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/insert?object_name=test_name_1&object_name=test_name_2&related_tasks=NaN'
                      '&active_days=0')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_basic_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'


@mark.regression
def test__regression__insert_empty_value():
    test_data = {'object_name': '', 'note': '', 'related_tasks': '', 'active_days': ''}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_same_record_two_times(database_with_one_record_added_by_api_call):
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "Object already exists"}]}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__find_basic_query(database_with_one_record_added_by_api_call):
    query = {'object_name': 'test_name'}
    return_data = get('http://0.0.0.0:7999/find', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"data": [{"object_name": "test_name", "note": "example_note", "related_tasks": "NaN", ' \
           '"active_days": "0"}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__find_wrong_keys():
    keys = ['note', 'related_tasks', 'active_days']
    for key in keys:
        query = {key: 'test_value'}
        return_data = get('http://0.0.0.0:7999/find', params=query)
        assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
        assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__find_empty_value():
    test_data = {'object_name': ''}
    return_data = get('http://0.0.0.0:7999/find', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__find_wrong_keys_in_payload():
    test_data = {'object': 'test_name'}
    return_data = get('http://0.0.0.0:7999/find', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__find_repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/find?object_name=test_name_1&object_name=test_name_2')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_basic_query(database_with_one_record_added_by_api_call):
    query = {'object_name': 'test_name'}
    return_data = get('http://0.0.0.0:7999/delete', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"status": "OK"}]}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_wrong_keys():
    keys = ['note', 'related_tasks', 'active_days']
    for key in keys:
        query = {key: 'test_value'}
        return_data = get('http://0.0.0.0:7999/delete', params=query)
        assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
        assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_empty_value():
    test_data = {'object_name': ''}
    return_data = get('http://0.0.0.0:7999/delete', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_wrong_keys_in_payload():
    test_data = {'object': 'test_name'}
    return_data = get('http://0.0.0.0:7999/delete', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/delete?object_name=test_name_1&object_name=test_name_2')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_nonexistent_record(database_with_one_record_added_by_api_call):
    query = {'object_name': 'nan'}
    return_data = get('http://0.0.0.0:7999/delete', params=query)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "No such object"}]}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_find_delete_record():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    query = {'object_name': 'test_name'}
    return_data = get('http://0.0.0.0:7999/find', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"data": [{"object_name": "test_name", "note": "example_note", "related_tasks": "NaN", ' \
           '"active_days": "0"}' in str(return_data.content), return_data.content
    return_data = get('http://0.0.0.0:7999/delete', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"status": "OK"}]}' in str(return_data.content), return_data.content
    return_data = get('http://0.0.0.0:7999/find', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"data": []}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_too_short_payload():
    test_data = {'username': ['test_user']}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_user_too_long_payload():
    test_data = {'username': ['test_user'], 'pass': ['11aa55ee22bb'], 'additional_key': ['value']}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_wrong_keys_in_payload():
    test_data = {'user': ['test_user'], 'password': ['11aa55ee22bb']}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/user_create?username=test_user_1&username=test_user_2&pass=11aa55ee22bb')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_basic_payload():
    test_data = {'username': 'test_user', 'pass': '11aa55ee22bb'}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'


@mark.regression
def test__regression__insert_user_empty_value():
    test_data = {'username': '', 'pass': ''}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__insert_user_same_record_two_times(database_with_one_record_added_by_api_call):
    test_data = {'username': 'test_user', 'pass': '11aa55ee22bb'}
    return_data = get('http://0.0.0.0:7999/user_create', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "User already exists"}]}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_user_basic_query(database_with_one_user_added_by_api_call):
    query = {'username': 'test_user'}
    return_data = get('http://0.0.0.0:7999/user_delete', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"status": "OK"}]}' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_user_empty_value():
    test_data = {'username': ''}
    return_data = get('http://0.0.0.0:7999/user_delete', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_user_wrong_keys_in_payload():
    query = {'user': 'test_user'}
    return_data = get('http://0.0.0.0:7999/user_delete', params=query)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_user_repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/user_delete?username=test_user_1&username=test_user_2')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.regression
def test__regression__delete_user_nonexistent_record(database_with_one_user_added_by_api_call):
    query = {'username': 'nan'}
    return_data = get('http://0.0.0.0:7999/user_delete', params=query)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "No such user"}]}' in str(return_data.content), return_data.content