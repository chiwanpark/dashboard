from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import os
import psutil
import time
import zlib


def get_cpu_stats():
    cpu = psutil.cpu_times_percent(interval=1, percpu=False)

    return {
        'user': cpu.user,
        'system': cpu.system,
        'idle': cpu.idle
    }


def get_mem_stats():
    virt = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        'virtual': {
            'total': virt.total,
            'available': virt.available,
            'used': virt.used
        },
        'swap': {
            'total': swap.total,
            'used': swap.used
        }
    }


def get_disk_stats():
    result = {}

    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.mountpoint)
        result[disk.device] = {
            'total': usage.total,
            'used': usage.used
        }

    return result


def get_net_stats():
    stat1 = psutil.net_io_counters()
    time.sleep(1)
    stat2 = psutil.net_io_counters()

    return {
        'bytes_sent': stat2.bytes_sent - stat1.bytes_sent,
        'bytes_recv': stat2.bytes_recv - stat1.bytes_recv,
        'packets_sent': stat2.packets_sent - stat1.packets_sent,
        'packets_recv': stat2.packets_recv - stat1.packets_recv
    }


def report(payload, hostname, auth_token):
    headers = {
        'Authorization': auth_token,
        'Content-Type': 'application/json',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'dashboard-metric-agent',
        'Content-Encoding': 'gzip',
    }

    payload = zlib.compress(payload, 9)
    url = 'https://dashboard.chiwanpark.com/metric/{}'.format(hostname)
    req = Request(url, data=payload, headers=headers, method='POST')
    try:
        resp = urlopen(req)
        if 'Content-Encoding: gzip' in resp.info().as_string():
            print('gzip compressed response')
            resp_payload = zlib.decompress(resp.read()).decode('utf-8')
        else:
            resp_payload = resp.read()
        print(json.loads(resp_payload))
    except HTTPError as e:
        print(e)


def main():
    hostname = os.environ['HOSTNAME']
    auth_token = os.environ['AUTH_TOKEN']

    payload = json.dumps({
        'cpu': get_cpu_stats(),
        'mem': get_mem_stats(),
        'disk': get_disk_stats(),
        'net': get_net_stats()
    }, check_circular=False, separators=(',', ':')).encode('utf-8')

    report(payload, hostname, auth_token)


if __name__ == '__main__':
    main()
