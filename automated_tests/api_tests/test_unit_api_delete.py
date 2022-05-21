from pytest import mark
from requests import get


@mark.unittest
def test__unit__basic_query(database_with_one_record_added_by_api_call):
    query = {'object_name': 'test_name'}
    return_data = get('http://0.0.0.0:7999/delete', params=query)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'
    assert '{"status": "OK"}]}' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__wrong_keys():
    keys = ['note', 'related_tasks', 'active_days']
    for key in keys:
        query = {key: 'test_value'}
        return_data = get('http://0.0.0.0:7999/delete', params=query)
        assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
        assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__empty_value():
    test_data = {'object_name': ''}
    return_data = get('http://0.0.0.0:7999/delete', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__wrong_keys_in_payload():
    test_data = {'object': 'test_name'}
    return_data = get('http://0.0.0.0:7999/delete', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/find?object_name=test_name_1&object_name=test_name_2')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content
