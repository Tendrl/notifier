from gevent.queue import Queue
import signal
from tendrl.alerting.exceptions import AlertingError
from tendrl.alerting.notification.exceptions import NotificationDispatchError
from tendrl.alerting.notification import NotificationPluginManager
from tendrl.alerting.watcher import AlertsWatchManager
from tendrl.alerting.handlers import AlertHandlerManager
from tendrl.alerting import AlertingNS
from tendrl.commons.event import Event
from tendrl.commons.message import ExceptionMessage
from tendrl.commons.message import Message
from tendrl.commons import TendrlNS


class TendrlAlertingManager(object):
    def __init__(self):
        try:
            NS.alert_queue = Queue()
            NS.alert_types = []
            NS.notification_medium = []
            self.alert_handler_manager = AlertHandlerManager()
            NS.notification_plugin_manager = NotificationPluginManager()
            self.watch_manager = AlertsWatchManager()
        except (AlertingError) as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Error intializing alerting manager',
                        "exception": ex
                    }
                )
            )
            raise ex

    def start(self):
        try:
            self.alert_handler_manager.start()
            self.watch_manager.run()
        except (
            AlertingError,
            NotificationDispatchError,
            Exception
        ) as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Error starting alerting manager',
                        "exception": ex
                    }
                )
            )
            raise ex

    def stop(self):
        try:
            self.watch_manager.stop()
        except Exception as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Exception stopping alerting',
                        "exception": ex
                    }
                )
            )
            raise ex


def main():
    AlertingNS()
    TendrlNS()
    NS.alerting.definitions.save()
    NS.alerting.config.save()
    NS.publisher_id = "alerting"

    tendrl_alerting_manager = TendrlAlertingManager()

    def terminate(sig, frame):
        Event(
            Message(
                "info",
                "alerting",
                {
                    "message": 'Signal handler: stopping',
                }
            )
        )
        tendrl_alerting_manager.stop()

    signal.signal(signal.SIGINT, terminate)
    tendrl_alerting_manager.start()


if __name__ == "__main__":
    main()
