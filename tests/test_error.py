from collections import namedtuple

import pytest

Case = namedtuple(
    'Case', ['method', 'url', 'params', 'data', 'detail', 'source'])

CASES = [
    Case(
        method='get',
        url='/tests/non-integer-string',
        data=None,
        params=None,
        detail="'non-integer-string' is not of type 'integer'",
        source={'parameter': 'test_id'},
    ),
    Case(
        method='get',
        url='/tests',
        params=None,
        data={},
        detail='search is a required parameter.',
        source={'parameter': 'search'},
    ),
    Case(
        method='get',
        url='/tests',
        params={'search': 'non-date-format-string'},
        data=None,
        detail="'non-date-format-string' is not a 'date'",
        source={'parameter': 'search'},
    ),
    Case(
        method='post_json',
        url='/tests',
        params=None,
        data={},
        detail="'data' is a required property",
        source={'pointer': ''},
    ),
    Case(
        method='post_json',
        url='/tests',
        params=None,
        data={
            'data': {
                'type': 'test',
                'attributes': {
                    'datetime': 'non-datetime-string',
                },
            },
        },
        detail="'non-datetime-string' is not a 'date-time'",
        source={'pointer': '/data/attributes/datetime'},
    ),
]


@pytest.mark.parametrize('method, url, params, data, detail, source', CASES)
def test_decorator_validation_error(
        method, url, params, data, source, detail, decorator_app):
    result = getattr(decorator_app, method)(url, params or data, status=400)
    error = result.json['errors'][0]
    assert error['detail'] == detail
    assert error['source'] == source


@pytest.mark.parametrize('method, url, params, data, detail, source', CASES)
def test_middleware_validation_error(
        method, url, params, data, source, detail, middleware_app):
    result = getattr(middleware_app, method)(url, params or data, status=400)
    error = result.json['errors'][0]
    assert error['detail'] == detail
    assert error['source'] == source


def test_no_operation_found(middleware_app):
    middleware_app.put('/missing_tests', status=404)


def test_undeclared_entrypoint(middleware_app):
    middleware_app.put('/backdoor', status=404)


def test_method_not_allowed(middleware_app):
    response = middleware_app.put('/tests', status=405)
    assert response.headers['Allow'] == 'GET, POST'
