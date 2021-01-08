import json
from collections import namedtuple

import pytest

Case = namedtuple(
    'Case', ['method', 'url', 'params', 'body', 'detail', 'source'])

CASES = [
    Case(
        method='simulate_get',
        url='/tests/non-integer-string',
        body=None,
        params=None,
        detail="'non-integer-string' is not of type 'integer'",
        source={'parameter': 'test_id'},
    ),
    Case(
        method='simulate_get',
        url='/tests',
        params=None,
        body='{}',
        detail='search is a required parameter.',
        source={'parameter': 'search'},
    ),
    Case(
        method='simulate_get',
        url='/tests',
        params={'clients': [5, 'non-integer-string'], 'search': '2016-12-20'},
        body=None,
        detail="'non-integer-string' is not of type 'integer'",
        source={'pointer': '/1'},
    ),
    Case(
        method='simulate_get',
        url='/tests',
        params={'search': 'non-date-format-string'},
        body=None,
        detail="'non-date-format-string' is not a 'date'",
        source={'parameter': 'search'},
    ),
    Case(
        method='simulate_post',
        url='/tests',
        params=None,
        body='{}',
        detail="'data' is a required property",
        source={'pointer': ''},
    ),
    Case(
        method='simulate_post',
        url='/tests',
        params=None,
        body=json.dumps({
            'data': {
                'type': 'test',
                'attributes': {
                    'datetime': 'non-datetime-string',
                },
            },
        }),
        detail="'non-datetime-string' is not a 'date-time'",
        source={'pointer': '/data/attributes/datetime'},
    ),
]


@pytest.mark.parametrize('method, url, params, body, detail, source', CASES)
def test_decorator_validation_error(
        method, url, params, body, source, detail, decorator_app):
    # pylint: disable=too-many-arguments
    handler = getattr(decorator_app, method)
    result = handler(url, body=body, params=params)
    assert result.status_code == 400
    error = result.json['errors'][0]
    assert error['detail'] == detail
    assert error['source'] == source


@pytest.mark.parametrize('method, url, params, body, detail, source', CASES)
def test_middleware_validation_error(
        method, url, params, body, source, detail, middleware_app):
    # pylint: disable=too-many-arguments,invalid-name
    handler = getattr(middleware_app, method)
    result = handler(url, body=body, params=params)
    assert result.status_code == 400
    error = result.json['errors'][0]
    assert error['detail'] == detail
    assert error['source'] == source


def test_no_operation_found(middleware_app):
    result = middleware_app.simulate_put('/missing_tests')
    assert result.status_code == 404


def test_undeclared_entrypoint(middleware_app):
    result = middleware_app.simulate_put('/backdoor')
    assert result.status_code == 404


def test_method_not_allowed(middleware_app):
    result = middleware_app.simulate_put('/tests')
    assert result.status_code == 405
    assert result.headers['Allow'] == 'GET, POST'
