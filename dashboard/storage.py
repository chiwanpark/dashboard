from google.cloud import datastore


datastore_client = datastore.Client()


def store_server_metric(hostname, timestamp, data):
    entity = datastore.Entity(key=datastore_client.key('ServerMetric', hostname, str(timestamp)))
    entity.update({
        'hostname': hostname,
        'timestamp': timestamp,
        'data': data
    })

    datastore_client.put(entity)
