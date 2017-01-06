from flask import Flask
from flask import request
from flask import Response
import logging
from multiprocessing import Event
from multiprocessing import Process
from tendrl.alerting.etcd.exceptions import EtcdError
from tendrl.alerting.etcd.manager import EtcdManager
from tendrl.alerting.exceptions import AlertingError
from tendrl.alerting.exceptions import InvalidRequest
from tendrl.alerting.notification.exceptions import InvalidHandlerConfig
from tendrl.alerting.notification.exceptions import NotificationPluginError
from tendrl.alerting.notification.manager import NotificationPluginManager
from tendrl.common.config import TendrlConfig


config = TendrlConfig()
LOG = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/alerting/notification_medium/supported")
def get_handlers():
    try:
        return Response(
            NotificationPluginManager().get_handlers(),
            mimetype='application/json'
        )
    except (
        AlertingError,
        NotificationPluginError
    ) as ex:
        raise ex


@app.route("/alerting/notification_medium/<name>/help")
def get_config_help(name):
    try:
        return Response(
            NotificationPluginManager().get_config_help(name),
            mimetype='application/json'
        )
    except (
        InvalidRequest,
        NotificationPluginError
    ) as ex:
        raise ex


@app.route("/alerting/alerts")
def get_alerts(filter_criteria=None):
    try:
        if len(request.args) > 0:
            return Response(
                str(EtcdManager().get_alerts(request.args.items())),
                mimetype='application/json'
            )
        return Response(
            str(EtcdManager().get_alerts()),
            mimetype='application/json'
        )
    except EtcdError as ex:
        raise ex


@app.route("/alerting/notification_medium/<name>/config", methods=['POST'])
def add_destination(name):
    try:
        return Response(
            NotificationPluginManager().add_destination(name, request.data),
            mimetype='application/json'
        )
    except (
        InvalidHandlerConfig,
        NotificationPluginError
    ) as ex:
        raise ex


@app.route("/alerting/alert_types")
def get_alert_types():
    try:
        return Response(
            str(EtcdManager().get_alert_types()),
            mimetype='application/json'
        )
    except EtcdError as ex:
        raise ex


class APIManager(Process):

    def __init__(self):
        super(APIManager, self).__init__()
        self._complete = Event()
        self.host = config.get(
            "alerting",
            "api_server_addr"
        )
        self.port = config.get(
            "alerting",
            "api_server_port"
        )

    def run(self):
        try:
            app.run(host=self.host, port=self.port)
            while not self._complete.is_set():
                self._complete.wait(timeout=1)
        except Exception as ex:
            LOG.error('Failed to start the api server. Error %s' %
                      ex, exc_info=True)
            self.terminate()
            raise ex
