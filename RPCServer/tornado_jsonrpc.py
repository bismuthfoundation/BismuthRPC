"""
json-rpc request handler for Tornado web application.

Based upon https://github.com/Pavel-Egorov/tornado_jsonrpc/
Copyright 2016 Pavel Egorov under the apache licence.
https://github.com/Pavel-Egorov/tornado_jsonrpc/blob/master/LICENSE

This file has been modified by @EggPool, the licence of the modified file is kept under apache licence.
"""

import json
# import sys, os
from copy import deepcopy
from logging import getLogger
from sys import exc_info

from base64 import b64decode

from tornado.web import RequestHandler

MAX_ERROR_MESSAGE_LENGTH = 200

# TODO: allow and process json-rpc 1.0
PROTOCOL_VERSIONS = ('2.0',)


# TODO: Handle proper auth

app_log = getLogger("tornado.application")


class JSONRPCHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def set_extra_headers(self, path=''):
        self.set_header('Cache-Control', 'no-store')

    def initialize(self, interface):
        self.interface = interface

    async def get(self):
        self.write("'JSON-RPC server handles only POST requests'")

    async def prepare(self):
        auth_header = self.request.headers.get("Authorization", "")
        # print("auth_header", auth_header)
        if not auth_header.startswith("Basic "):
            self.set_status(401)
            # self.write("'Auth required {}'".format(auth_header))
            self.finish()
        auth_decoded = b64decode(auth_header[6:]).decode('ascii')
        username, password = str(auth_decoded).split(':', 1)
        # print(username, password)
        if (username, password) != (self.interface.config.rpcuser, self.interface.config.rpcpassword):
            print("Auth failed")
            self.set_status(403)
            # self.write("'Auth Failed'")
            self.finish()

    async def post(self, *args, **kwargs):
        try:
            request_body = json.loads(self.request.body.decode())
            if self.interface.config.verbose > 1:
                app_log.info("request_body {}", self.request.body.decode())
            if not request_body:
                raise InvalidJSON

            is_list = isinstance(request_body, list)
            is_dict = isinstance(request_body, dict)

            if not (is_dict or is_list):
                raise InvalidJSON
        except (UnicodeDecodeError, json.JSONDecodeError) as exception:
            self.write({'id': None, 'result': None, 'error': _get_error(exception)})
            return

        if is_dict:
            response = await _get_response(self, self.interface, request_body)
            if response:
                self.write(response)
        elif is_list:
            responses = []

            for i in request_body:
                response = await _get_response(self, self.interface, i)
                if response:
                    responses.append(response)

            if responses:
                self.write(json.dumps(responses).encode())


class CORSIgnoreJSONRPCHandler(JSONRPCHandler):
    def set_default_headers(self):
        super().set_default_headers()
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'POST, OPTIONS')

    def options(self):
        pass


class WithCredentialsJSONRPCHandler(CORSIgnoreJSONRPCHandler):
    def set_default_headers(self):
        super().set_default_headers()
        self.set_header('withCredentials', 'true')


def _get_error(exception):
    return {
        'code': getattr(exception, 'code', InternalError.code),
        'message': getattr(exception, 'message', str(exc_info()[0]))[:MAX_ERROR_MESSAGE_LENGTH],
        'data': getattr(exception, 'data', None)
    }


async def _get_response(request, interface, request_body):
    version = None
    request_id = None

    try:
        request_id = request_body.get('id')
        version = _get_version(request_body)
        if interface.config.verbose:
            app_log.info("request_id {} version {}".format(request_id, version))
        result = await _get_result(request, _get_method(interface, request_body), request_body.get('params'))
        if interface.config.verbose:
            app_log.info("result {}".format(json.dumps(result)))
    except Exception as exception:
        if interface.config.verbose:
            app_log.warning("Exception {}".format(exception))
        return _get_with_protocol_version({'id': request_id, 'result': None, 'error': _get_error(exception)}, version)

    if request_id:
        return _get_with_protocol_version({'id': request_id, 'result': result, 'error': None}, version)


def _get_method(interface, request_body):
    if interface.config.verbose > 1:
        app_log.info("Looking for method {}".format(request_body.get('method', '')))
    method = getattr(interface, request_body.get('method', ''), None)
    if not method:
        raise MethodNotFound
    return method


def _get_version(request_body):
    version = request_body.get('jsonrpc')
    if version and version not in PROTOCOL_VERSIONS:
        raise InvalidVersion
    return version


async def _get_result(request, method, params):
    if params is None:
        return await method(request)

    elif isinstance(params, list):
        return await method(request, *params)

    elif isinstance(params, dict):
        return await method(request, **params)
    raise InvalidParams


def _get_with_protocol_version(response, version):
    updated_response = deepcopy(response)
    if version:
        updated_response['jsonrpc'] = version
    return updated_response


class InvalidVersion(Exception):
    code = -32600
    message = 'Invalid Request'
    data = None


class MethodNotFound(Exception):
    code = -32601
    message = 'Method not found'
    data = None


class InvalidParams(Exception):
    code = -32602
    message = 'Invalid params'
    data = None


class InternalError(Exception):
    code = -32603
    message = 'Internal error'
    data = None


class InvalidJSON(Exception):
    code = -32700
    message = 'Parse error'
    data = None
