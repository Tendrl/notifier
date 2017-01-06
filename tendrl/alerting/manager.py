import logging
import multiprocessing
import signal
from tendrl.alerting.api.manager import APIManager
from tendrl.alerting.etcd.manager import EtcdManager
from tendrl.alerting.exceptions import AlertingError
from tendrl.alerting.notification.exceptions import NotificationDispatchError
from tendrl.alerting.notification.manager import NotificationPluginManager
from tendrl.alerting.watcher.manager import AlertsWatchManager
from tendrl.common.config import TendrlConfig
from tendrl.common import log


LOG = logging.getLogger(__name__)
config = TendrlConfig()


class Manager(object):
    def __init__(self):
        try:
            self.api_manager = APIManager()
            self.alert_queue = multiprocessing.Queue()
            self.watch_manager = AlertsWatchManager(self.alert_queue)
            EtcdManager().write_configs()
            EtcdManager().load_defs()
        except AlertingError as ex:
            raise ex

    def start(self):
        try:
            self.api_manager.start()
            self.watch_manager.start()
            NotificationPluginManager().start(self.alert_queue)
        except (
            AlertingError,
            NotificationDispatchError,
            Exception
        ) as ex:
            LOG.error(
                'Exception %s' % str(ex),
                exc_info=True
            )
            raise ex

    def stop(self):
        try:
            self.alert_queue.close()
            self.api_manager.terminate()
            NotificationPluginManager().stop()
            self.watch_manager.terminate()
        except Exception as ex:
            LOG.error(
                'Exception %s' % str(ex),
                exc_info=True
            )
            raise ex


def main():
    log.setup_logging(
        config.get('alerting', 'log_cfg_path'),
        config.get('alerting', 'log_level')
    )
    manager = Manager()

    def terminate(sig, frame):
        LOG.error("Signal handler: stopping", exc_info=True)
        manager.stop()

    signal.signal(signal.SIGINT, terminate)
    manager.start()


if __name__ == "__main__":
    main()
