Falguard |travis| |codecov| |python-versions|
=============================================

Falguard is a Python library that provides request validation helpers for
`Falcon <https://falconframework.org/>`_ web framework. Falguard relies on Yelp's `bravado-core <https://github.com/Yelp/bravado-core>`_ library.

Features
--------
* Validation of `OpenAPI (Swagger) <http://swagger.io/specification/>`_ schema
* Error serialization compliant with `JSON:API <http://jsonapi.org/format/#error-objects>`_ specification
* Validator may be used either as a hook or a middleware component

Installation
------------
.. code:: bash

    $ pip install falguard

Usage
-----
Instantiate Validator with the path to OpenAPI specification...

.. code:: python

    import falguard

    validator = falguard.Validator('spec.json')


...and use it as the hook on the responder...

.. code:: python

    class Resource:

        @falcon.before(validator)
        def on_get(self, request, response, **validated):
            pass


...or the hook on the whole resource...

.. code:: python

    @falcon.before(validator)
    class Resource:
        pass


...or globally, as the middleware component.

.. code:: python

    import falcon

    api = falcon.API(middleware=validator)


All validated parameters (path, query, body) are injected back to the responder
so it MUST accept relevant number of arguments, eg.

.. code:: python

    class Resource:

        def on_put(self, request, response, resource_id, data):
            pass

        def on_post(self, request, response, **validated):
            pass

.. |travis| image:: https://travis-ci.org/gwaramadze/falguard.svg
   :target: https://travis-ci.org/gwaramadze/falguard

.. |codecov| image:: https://codecov.io/gh/gwaramadze/falguard/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/gwaramadze/falguard

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/falguard.svg
    :target: https://pypi.org/project/falguard/
