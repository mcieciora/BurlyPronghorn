from pytest import mark, raises
from requests import get
from src.api import Api, Delete, Find, Insert


@mark.unittest
def test__unit__api_verify_payload_and_action():
    test_object = Api({})
    assert test_object.verify_payload() is None, f'Incorrect verify_payload return: {test_object}'
    return_data = test_object.action()
    assert return_data == {'data': [{'status': 'OK'}]}, f'Incorrect return data {return_data}'


@mark.unittest
def test__unit__find_verify_payload_and_action():
    test_data_with_expected_results = {
        'basic_payload':
            {'data': {'object_name': ['test_name']}, 'result': True},
        'empty_payload':
            {'data': {}, 'result': True},
        'wrong_keys':
            {'data': {'object': ['test_name']}, 'result': False},
        'empty_value':
            {'data': {'object_name': ['']}, 'result': False}
    }
    for key, test_data in test_data_with_expected_results.items():
        test_object = Find(test_data['data'])
        assert test_object.verify_payload() is test_data['result'], f'Incorrect verify_payload return for {test_data}'
        del test_object
    with raises(ValueError):
        Find({'object_name': ['test_name_1', 'test_name_2']})
    test_object = Find(test_data_with_expected_results['basic_payload']['data'])
    return_data = test_object.action()
    assert return_data == {'data': []}, f'Incorrect return data {return_data}'


@mark.unittest
def test__unit__insert_verify_payload_and_action():
    test_data_with_expected_results = {
        'basic_payload':
            {'data': {'object_name': ['test_name'], 'note': ['example_note'], 'related_tasks': ['NaN'],
                      'active_days': ['0']}, 'result': True},
        'short_payload':
            {'data': {'object_name': ['test_name'], 'note': ['example_note'], 'related_tasks': ['NaN']},
             'result': False},
        'too_long_payload':
            {'data': {'object_name': ['test_name'], 'note': ['example_note'], 'related_tasks': ['NaN'],
                      'active_days': ['0'], 'additional_key': ['value']}, 'result': False},
        'wrong_keys':
            {'data': {'object_name': ['test_name'], 'note': ['example_note'], 'tasks': ['NaN'], 'active_days': ['0']},
             'result': False},
        'empty_value':
            {'data': {'object_name': [''], 'note': [''], 'related_tasks': [''], 'active_days': ['']}, 'result': False}
    }
    for test_data in test_data_with_expected_results.values():
        test_object = Insert(test_data['data'])
        assert test_object.verify_payload() is test_data['result'], f'Incorrect verify_payload return for {test_data}'
        del test_object
    with raises(ValueError):
        Find({'object_name': ['test_name_1', 'test_name_2'], 'note': ['example_note'], 'related_tasks': ['NaN'],
              'active_days': ['0']})
    test_object = Insert(test_data_with_expected_results['basic_payload']['data'])
    return_data = test_object.action()
    assert return_data == {'status': 'OK'}, f'Incorrect return data {return_data}'
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    get('http://0.0.0.0:7999/insert', params=test_data)
    assert test_object.verify_payload() is True, f'Incorrect verify_payload return for {test_data}'
    return_data = test_object.action()
    assert return_data == {'data': [{'status': 'OK'}]}, f'Incorrect return data {return_data}'


@mark.unittest
def test__unit__delete_verify_payload_and_action():
    test_data_with_expected_results = {
        'basic_payload':
            {'data': {'object_name': ['test_name']}, 'result': True},
        'empty_payload':
            {'data': {}, 'result': True},
        'wrong_keys':
            {'data': {'object': ['test_name']}, 'result': False},
        'empty_value':
            {'data': {'object_name': ['']}, 'result': False}
    }
    for test_data in test_data_with_expected_results.values():
        test_object = Delete(test_data['data'])
        assert test_object.verify_payload() is test_data['result'], f'Incorrect verify_payload return for {test_data}'
        del test_object
    with raises(ValueError):
        Find({'object_name': ['test_name_1', 'test_name_2']})
    test_object = Delete(test_data_with_expected_results['basic_payload']['data'])
    return_data = test_object.action()
    assert return_data == {'data': [{'status': 'OK'}]}, f'Incorrect return data {return_data}'
