from dashboard import storage
from flask import current_app as app
from flask import Blueprint, abort, jsonify, make_response, request
from time import time
import json
import zlib


blueprint = Blueprint('metric', __name__, url_prefix='/metric')


@blueprint.after_request
def _after_request(response):
    valid = 'gzip' in request.headers.get('Accept-Encoding', '')
    valid &= 200 <= response.status_code and response.status_code < 300

    if valid:
        app.logger.info('Compress response via zlib')
        response.data = zlib.compress(response.data, 9)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(response.data)

    return response


def is_secure_request(hostname):
    auth_token = request.headers.get('Authorization', None)
    if not auth_token:
        app.logger.info('No Authorization header')
        return False

    secure_key = storage.get_secure_key('metric-{}'.format(hostname))
    if not secure_key or secure_key['auth_token'] != auth_token:
        app.logger.info('Secure key mismatch')
        return False

    return True


@blueprint.route('/<hostname>', methods=['POST'])
def add_metric(hostname):
    if not is_secure_request(hostname):
        abort(401)

    if request.headers.get('Content-Encoding', '') == 'gzip':
        try:
            data = json.loads(zlib.decompress(request.data))
        except (ValueError, zlib.error):
            data = None
    else:
        data = request.get_json()
    if not data:
        abort(400)
    timestamp = time()

    try:
        storage.store_server_metric(hostname, timestamp, data)
        return jsonify(success=True)
    except ValueError:
        return make_response(jsonify(success=False), 500)
