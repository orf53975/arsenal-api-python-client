"""
This module contains Log API functions.
"""
from .arsenal import ArsenalObject

class Log(ArsenalObject):
    """
    This object represents a Log from the teamserver.
    """

    timestamp = None
    application = None
    level = None
    message = None

    @staticmethod
    def create_log(
            application,
            level,
            message):
        """
        Generate a log on the teamserver.
        """
        resp = ArsenalObject._call(
            'CreateLog',
            application=application,
            level=level,
            message=message)

        if resp.get('error', True):
            print('ERROR: Could not create log. {}'.format(resp.get('description')))

    @staticmethod
    def list_logs(
            application=None,
            since=None,
            include_archived=None):
        """
        List logs from the teamserver, optionally filtering.
        """
        resp = ArsenalObject._call(
            'ListLogs',
            application=application,
            since=since,
            include_archived=include_archived)

        if resp.get('error', True):
            print('ERROR: Could not list logs. {}'.format(resp.get('description')))

        return [Log(log_data) for log_data in resp['logs']]