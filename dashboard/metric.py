from dashboard.storage import get_secure_key, store_server_metric
from flask import current_app as app
from flask import Blueprint, abort, jsonify, make_response, request
from time import time


blueprint = Blueprint('metric', __name__, url_prefix='/metric')


def is_secure_request(hostname):
    auth_token = request.headers.get('Authorization', None)
    if not auth_token:
        app.logger.info('No Authorization header')
        return False

    secure_key = get_secure_key('metric-{}'.format(hostname))
    if not secure_key or secure_key['auth_token'] != auth_token:
        app.logger.info('Secure key mismatch')
        return False

    return True


@blueprint.route('/<hostname>', methods=['POST'])
def add_metric(hostname):
    if not is_secure_request(hostname):
        abort(401)

    data = request.get_json()
    if not data:
        abort(400)
    timestamp = time()

    try:
        store_server_metric(hostname, timestamp, data)
        return jsonify(success=True)
    except ValueError:
        return make_response(jsonify(success=False), 500)
