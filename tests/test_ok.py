import json
from collections import namedtuple

import pytest

Case = namedtuple('Case', ['method', 'url', 'params', 'body'])

CASES = [
    Case(
        method='simulate_get',
        url='/tests/7',
        params=None,
        body=None,
    ),
    Case(
        method='simulate_get',
        url='/tests',
        params={'search': '2016-12-20'},
        body=None
    ),
    Case(
        method='simulate_post',
        url='/tests',
        params=None,
        body=json.dumps({
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
        }),
    ),
]


@pytest.mark.parametrize('method, url, params, body', CASES)
def test_decorator_validation_ok(method, url, params, body, decorator_app):
    handler = getattr(decorator_app, method)
    result = handler(url, params=params, body=body)
    assert result.status_code == 200


@pytest.mark.parametrize('method, url, params, body', CASES)
def test_middleware_validation_ok(method, url, params, body, middleware_app):
    handler = getattr(middleware_app, method)
    result = handler(url, params=params, body=body)
    assert result.status_code == 200
