import requests
from requests import ReadTimeout, ConnectionError

from nvgpu.list_gpus import format_table, device_table


def format_reports_to_ansi(hosts, reports):
    def format_report(host, report):
        if 'error' not in report:
            return '\n'.join([report['hostname'], format_table(device_table(report['gpus']))])
        else:
            return '\n'.join([host, report['error']])

    return '\n\n'.join([
        format_report(host, report)
        for host, report in zip(hosts, reports)])


def gather_reports(hosts):
    return [download_report(host) for host in hosts]


def download_report(host):
    try:
        resp = requests.get(host + '/gpu_status', timeout=5)
        if resp.status_code != 200:
            return {'error': 'Bad response (%s: %s)' % (resp.status_code, resp.reason)}
    except ConnectionError:
        return {'error': 'Host not available'}
    except ReadTimeout:
        return {'error': 'Connection timeout'}

    return resp.json()
