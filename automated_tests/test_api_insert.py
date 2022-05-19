from pytest import mark
from requests import get


@mark.unit
def test__unit__too_short_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'NaN', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'


@mark.unit
def test__unit__too_long_payload():
    pass


@mark.unit
def test__unit__wrong_keys_in_payload():
    pass


@mark.unit
def test__unit__repeated_keys_in_payload():
    pass


@mark.unit
def test__unit__basic_payload():
    test_data = {'object_name': 'test_name', 'note': 'example_note', 'related_tasks': 'a', 'active_days': '0'}
    return_data = get('http://0.0.0.0:7999/insert', params=test_data)
    assert return_data.status_code == 200, f'Status code is not 200: {return_data.reason}'


@mark.unit
def test__unit__non_existing_request_type():
    pass


@mark.unit
def test__unit__empty_value():
    pass


@mark.unit
def test__unit__all_requests_types_proper_responses():
    pass


@mark.unit
def test__unit__all_requests_types_distorted_responses():
    pass
