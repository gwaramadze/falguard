import datetime
from dateutil.tz import tzoffset

import falcon
import pytest
import webtest

import falguard

VALIDATORS = [
    falguard.Validator('tests/specs/spec.json'),
    falguard.Validator('tests/specs/spec.yaml'),
    falguard.Validator('tests/specs/spec.yml'),
]


class _CollectionResource(object):

    def on_get(self, request, response, search):
        # pylint: disable=unused-argument,no-self-use
        assert search == datetime.date(2016, 12, 20)

    def on_post(self, request, response, data):
        # pylint: disable=unused-argument,no-self-use
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


class _ElementResource(object):

    def on_get(self, request, response, test_id):
        # pylint: disable=unused-argument,no-self-use
        assert test_id == 7


@pytest.fixture(params=VALIDATORS)
def decorator_app(request):
    validator = request.param

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


@pytest.fixture(params=VALIDATORS)
def middleware_app(request):
    validator = request.param
    api = falcon.API(middleware=validator)
    api.add_route('/tests', _CollectionResource())
    api.add_route('/tests/{test_id}', _ElementResource())
    # add entry point not in the specs
    api.add_route('/backdoor', _CollectionResource())
    return webtest.TestApp(api)
