import multiprocessing
import os
import signal
from tendrl.alerting.central_store import AlertingEtcdPersister
from tendrl.alerting.exceptions import AlertingError
from tendrl.alerting.notification.exceptions import NotificationDispatchError
from tendrl.alerting.notification import NotificationPluginManager
from tendrl.alerting.watcher import AlertsWatchManager
from tendrl.alerting.handlers import AlertHandlerManager
from tendrl.commons.event import Event
from tendrl.commons.message import Message


class TendrlAlertingManager(object):
    def __init__(self):
        try:
            tendrl_ns.alert_queue = multiprocessing.Queue()
            tendrl_ns.alert_types = []
            tendrl_ns.notification_medium = []
            self.alert_handler_manager = AlertHandlerManager()
            tendrl_ns.notification_plugin_manager = NotificationPluginManager()
            self.watch_manager = AlertsWatchManager()
        except (AlertingError) as ex:
            Event(
                Message(
                    "error",
                    "alerting",
                    {
                        "message": 'Exception %s' % str(ex),
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
                Message(
                    "error",
                    "alerting",
                    {
                        "message": 'Exception %s' % str(ex),
                    }
                )
            )
            raise ex

    def stop(self):
        try:
            tendrl_ns.alert_queue.close()
            self.watch_manager.stop()
            os.system("ps -C tendrl-alerting -o pid=|xargs kill -9")
        except Exception as ex:
            Event(
                Message(
                    "error",
                    "alerting",
                    {
                        "message": 'Exception %s' % str(ex),
                    }
                )
            )
            raise ex


def main():
    tendrl_ns.central_store_thread = AlertingEtcdPersister()
    tendrl_ns.definitions.save()
    tendrl_ns.config.save()

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
