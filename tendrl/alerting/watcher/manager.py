import etcd
import logging
import multiprocessing
from tendrl.alerting.exceptions import AlertingError
from tendrl.common.alert import Alert
from tendrl.common.config import ConfigNotFound
from tendrl.common.config import TendrlConfig

config = TendrlConfig()
LOG = logging.getLogger(__name__)


class AlertsWatchManager(multiprocessing.Process):
    def __init__(self, alert_queue):
        super(AlertsWatchManager, self).__init__()
        self.alert_queue = alert_queue
        try:
            etcd_kwargs = {
                'port': int(config.get("common", "etcd_port")),
                'host': config.get("common", "etcd_connection")
            }
            self.etcd_client = etcd.Client(**etcd_kwargs)
        except ConfigNotFound as ex:
            LOG.error(
                'Intialization of alerts watcher failed. Error %s' % str(ex),
                exc_info=True
            )
            raise AlertingError(str(ex))

    def run(self):
        while True:
            new_alert = self.etcd_client.watch(
                '/alerts',
                recursive=True,
                timeout=0
            )
            if new_alert is not None:
                if new_alert.value is not None:
                    self.alert_queue.put(Alert.to_obj(str(new_alert.value)))
