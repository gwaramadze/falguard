import datetime
from dateutil.tz import tzoffset

import falcon
import pytest
import webtest

import falguard

validator = falguard.Validator('tests/spec.json')


class _CollectionResource:

    def on_get(self, request, response, search):
        assert search == datetime.date(2016, 12, 20)

    def on_post(self, request, response, data):
        assert data == {
            'id': None,
            'type': 'tests',
            'attributes': {
                'integer': 7,
                'float': 7.7777,
                'string': 'random string',
                'boolean': True,
                'datetime': datetime.datetime(
                    2016, 12, 18, 22, 48, 5, tzinfo=tzoffset(None, 7200)),
            },
        }


class _ElementResource:

    def on_get(self, request, response, test_id):
        assert test_id == 7


@pytest.fixture
def decorator_app():

    @falcon.before(validator)
    class _DecoratedCollectionResource(_CollectionResource):
        pass

    @falcon.before(validator)
    class _DecoratedElementResource(_ElementResource):
        pass

    api = falcon.API()
    api.add_route('/tests', _DecoratedCollectionResource())
    api.add_route('/tests/{test_id}', _DecoratedElementResource())
    return webtest.TestApp(api)


@pytest.fixture
def middleware_app():
    api = falcon.API(middleware=validator)
    api.add_route('/tests', _CollectionResource())
    api.add_route('/tests/{test_id}', _ElementResource())
    return webtest.TestApp(api)
