from pytest import mark
from requests import get


@mark.unittest
def test__unit__too_short_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__too_long_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0',
                 'additional_key': 'value'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__wrong_keys_in_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__repeated_keys_in_payload():
    return_data = get('http://0.0.0.0:7999/insert?object_name=test_name_1&object_name=test_name_2&related_tasks=NaN'
                      '&active_days=0')
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content


@mark.unittest
def test__unit__basic_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'


@mark.unittest
def test__unit__empty_value():
    test_data = {'object_name': '', 'note': '', 'related_tasks': '', 'active_days': ''}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert 'Incorrect payload' in str(return_data.content), return_data.content
