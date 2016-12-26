from collections import namedtuple

import pytest

Case = namedtuple('Case', ['method', 'url', 'data_or_params'])

CASES = [
    Case(
        method='get',
        url='/tests/7',
        data_or_params=None,
    ),
    Case(
        method='get',
        url='/tests',
        data_or_params={'search': '2016-12-20'},
    ),
    Case(
        method='post_json',
        url='/tests',
        data_or_params={
            'data': {
                'type': 'tests',
                'attributes': {
                    'integer': 7,
                    'float': 7.7777,
                    'string': 'random string',
                    'boolean': True,
                    'datetime': '2016-12-18T22:48:05+02:00',
                },
            },
        },
    ),
]


@pytest.mark.parametrize('method, url, data_or_params', CASES)
def test_decorator_validation_ok(method, url, data_or_params, decorator_app):
    getattr(decorator_app, method)(url, data_or_params)


@pytest.mark.parametrize('method, url, data_or_params', CASES)
def test_middleware_validation_ok(method, url, data_or_params, middleware_app):
    getattr(middleware_app, method)(url, data_or_params)
