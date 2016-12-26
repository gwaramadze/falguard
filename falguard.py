import io
import json

from bravado_core.request import IncomingRequest, unmarshal_request
from bravado_core.spec import Spec
import falcon
from jsonschema.exceptions import ValidationError


class _BravadoRequest(IncomingRequest):

    def __init__(self, falcon_request, path_parameters):
        self.path = path_parameters
        self.query = falcon_request.params
        self.headers = falcon_request.headers

        # Non-reusable Falcon stream is replaced with reusable alternative
        falcon_request.stream = io.BytesIO(falcon_request.stream.read())
        data = falcon_request.stream.getvalue().decode()
        try:
            self.form = json.loads(data)
        except ValueError:
            self.form = None

        # TODO: not supported
        self.files = None

    def json(self):
        return self.form


class _JsonApiErrorResponseFormatter:

    def format(self, validation_error, obj_type):
        error = obj_type()
        error['detail'] = validation_error.message.replace("u'", "'")
        error['source'] = self._get_source(validation_error)
        return {'errors': [error]}

    def _get_source(self, validation_error):
        path = '/'.join(validation_error.path)
        if path:
            return {'pointer': '/' + path}
        parameter = validation_error.schema.get('name')
        if parameter:
            return {'parameter': parameter}
        return {'pointer': ''}


class _HTTPBadRequest(falcon.HTTPBadRequest):

    _formatter = _JsonApiErrorResponseFormatter()

    def __init__(self, validation_error):
        super(_HTTPBadRequest, self).__init__()
        self._validation_error = validation_error

    def to_dict(self, obj_type=dict):
        return self._formatter.format(self._validation_error, obj_type)


class Validator:

    def __init__(self, spec_path):
        with open(spec_path, 'r') as f:
            spec_dict = json.loads(f.read())
        self._spec = Spec.from_dict(spec_dict, config={'use_models': False})

    def __call__(self, request, response, resource, params):
        self.process_resource(request, response, resource, params)

    def process_resource(self, request, response, resource, params):
        bravado_request = _BravadoRequest(request, params)

        operation = self._spec.get_op_for_request(
            request.method.upper(), request.uri_template)
        if not operation:
            raise falcon.HTTPNotFound

        try:
            validated = unmarshal_request(bravado_request, operation)
        except ValidationError as e:
            raise _HTTPBadRequest(e)
        else:
            body = validated.pop('body', None)
            if body:
                validated.update(body)
            params.clear()
            params.update(validated)
