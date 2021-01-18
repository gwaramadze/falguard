import functools
import io
import json
import os
import yaml

from bravado_core.request import IncomingRequest, unmarshal_request
from bravado_core.spec import Spec
import falcon
from falcon import HTTP_METHODS  # pylint: disable=no-name-in-module
from jsonschema.exceptions import ValidationError


DESERIALIZERS = {
    '.json': json.loads,
    '.yaml': yaml.safe_load,
    '.yml': yaml.safe_load,
}


class _BravadoRequest(IncomingRequest):

    def __init__(self, falcon_request, path_parameters):
        self.path = path_parameters
        self.query = falcon_request.params
        self.headers = falcon_request.headers

        # Non-reusable Falcon stream is replaced with reusable alternative
        falcon_request.stream = io.BytesIO(
            falcon_request.bounded_stream.read())
        data = falcon_request.stream.getvalue().decode()
        try:
            self.form = json.loads(data)
        except ValueError:
            self.form = None

        # TODO: not supported
        self.files = None

    def json(self, **kwargs):
        return self.form


class _JsonApiErrorResponseFormatter(object):

    def format(self, validation_error, obj_type):
        error = obj_type()
        error['detail'] = validation_error.message.replace("u'", "'")
        error['source'] = self._get_source(validation_error)
        return {'errors': [error]}

    def _get_source(self, validation_error):
        # pylint: disable=no-self-use
        path = '/'.join(map(str, validation_error.path))
        if path:
            return {'pointer': '/' + path}
        parameter = validation_error.schema.get('name')
        if parameter:
            return {'parameter': parameter}
        return {'pointer': ''}


class _HTTPBadRequest(falcon.errors.HTTPBadRequest):

    _formatter = _JsonApiErrorResponseFormatter()

    def __init__(self, validation_error):
        # pylint: disable=super-with-arguments
        super(_HTTPBadRequest, self).__init__()
        self._validation_error = validation_error

    def to_dict(self, obj_type=dict):
        return self._formatter.format(self._validation_error, obj_type)


class Validator(object):
    def __init__(self, spec_path):
        _, ext = os.path.splitext(spec_path)
        with open(spec_path, 'r') as f:
            spec_dict = DESERIALIZERS[ext](f.read())
        self._spec = Spec.from_dict(spec_dict, config={'use_models': False})

    def __call__(self, request, response, resource, params):
        self.process_resource(request, response, resource, params)

    def process_resource(self, request, response, resource, params):
        # pylint: disable=unused-argument
        bravado_request = _BravadoRequest(request, params)

        get_op = functools.partial(
            self._spec.get_op_for_request,
            path_pattern=request.uri_template,
        )

        operation = get_op(request.method)
        if not operation:
            # The URI exists but the method is wrong.
            # So we are going to reply with an error 405.
            # Error 405 requires we provide the list of allowed methods
            # for this URI. If None is found, then we produce a 404 error.
            allowed = [m for m in HTTP_METHODS if get_op(m)]
            if allowed:
                raise falcon.errors.HTTPMethodNotAllowed(allowed)
            raise falcon.errors.HTTPNotFound

        try:
            validated = unmarshal_request(bravado_request, operation)
        # pylint: disable=raise-missing-from
        except ValidationError as e:
            raise _HTTPBadRequest(e)
        else:
            body = validated.pop('body', None)
            if body:
                validated.update(body)
            params.clear()
            params.update(validated)
