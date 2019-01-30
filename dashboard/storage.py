from google.cloud import datastore


_client = datastore.Client()


def store_server_metric(hostname, timestamp, data):
    entity = datastore.Entity(_client.key('ServerMetric'))
    entity.update({
        'hostname': hostname,
        'timestamp': timestamp,
        'data': data
    })

    _client.put(entity)

    return entity.key


def get_secure_key(client_name):
    key = _client.key('ClientSecure', client_name)
    entity = _client.get(key)
    if not entity:
        return None
    return entity
