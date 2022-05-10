from pytest import mark
from requests import get


@mark.unit
def test__unit__too_short_payload():
    pass


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
    pass


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
