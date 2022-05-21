from pytest import mark
from requests import get


@mark.regular
def test__regular__insert_find_delete_record():
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


@mark.skip
@mark.regular
def test__regular__insert_same_record_two_times(database_with_one_record_added_by_api_call):
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "Object already exists"}]}' in str(return_data.content), return_data.content


@mark.skip
@mark.regular
def test__unit__delete_nonexistent_record(database_with_one_record_added_by_api_call):
    query = {'object_name': 'test_name'}
    return_data = get('http://0.0.0.0:7999/delete', params=query)
    assert return_data.status_code == 400, f'Status code is not 400: {return_data.reason}'
    assert '{"status": "No such object"}]}' in str(return_data.content), return_data.content
