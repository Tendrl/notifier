import multiprocessing
from tendrl.commons.etcdobj import Server as etcd_server
from tendrl.commons.event import Event
from tendrl.commons.message import ExceptionMessage


class AlertsWatchManager(multiprocessing.Process):
    def __init__(self):
        super(AlertsWatchManager, self).__init__()
        etcd_kwargs = {
            'port': int(NS.alerting.config.data["etcd_port"]),
            'host': NS.alerting.config.data["etcd_connection"]
        }
        self.etcd_client = etcd_server(etcd_kwargs=etcd_kwargs).client
        self.complete = multiprocessing.Event()
        self.handled_msgs = []

    def run(self):
        try:
            while not self.complete.is_set():
                new_message = self.etcd_client.watch(
                    '/messages/events',
                    recursive=True,
                    timeout=0
                )
                if (
                    new_message is None or
                    str(new_message.action) == 'delete' or
                    not new_message
                ):
                    continue
                msg_parts = new_message.key.split('/')
                if (
                    new_message.key.startswith('/messages/events') and
                    len(msg_parts) >= 4
                ):
                    message_id = msg_parts[3]
                    if message_id not in self.handled_msgs:
                        self.handled_msgs.append(message_id)
                        NS.alert_queue.put(message_id)
        except Exception as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Exception in alert watcher',
                        "exception": ex
                    }
                )
            )
            raise ex

    def stop(self):
        self.complete.set()
