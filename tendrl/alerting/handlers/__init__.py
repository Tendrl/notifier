import etcd
import importlib
import inspect
import json
import multiprocessing
import os
import six
from tendrl.alerting import constants
from tendrl.alerting.objects.alert import AlertUtils
from tendrl.commons.event import Event
from tendrl.commons.message import ExceptionMessage
from tendrl.commons.message import Message
from tendrl.commons.utils.time_utils import now
import time


class NoHandlerException(Exception):
    pass


class HandlerMount(type):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'handlers'):
            cls.handlers = []
        else:
            cls.register_handler(cls)

    def register_handler(cls, handler):
        instance = handler()
        cls.handlers.append(instance)


@six.add_metaclass(HandlerMount)
class AlertHandler(object):

    handles = ''
    representive_name = ''

    def __init__(self):
        self.time_stamp = now()
        self.alert = None

    def update_alert(self):
        # Fetch alerts in etcd
        try:
            alerts = tendrl_ns.central_store_thread.get_alerts()
            # Check if similar alert already exists
            for curr_alert in alerts:
                # If similar alert exists, update the similar alert to etcd
                if AlertUtils().is_same(self.alert, curr_alert):
                    self.alert = AlertUtils().update(
                        self.alert,
                        curr_alert
                    )
                    if not AlertUtils().equals(
                        self.alert,
                        curr_alert
                    ):
                        self.alert.save()
                    return
                # else add this new alert to etcd
            self.alert.save()
        except etcd.EtcdKeyNotFound:
            try:
                self.alert.save()
            except Exception as ex:
                Event(
                    ExceptionMessage(
                        priority="error",
                        publisher="alerting",
                        payload={
                            "message": "Exception %s in handler",
                            "exception": ex
                        }
                    )
                )
        except (etcd.EtcdConnectionFailed, Exception) as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Failed to fetch existing alerts.',
                        "exception": ex
                    }
                )
            )

    def handle(self, alert_obj):
        try:
            self.alert = alert_obj
            self.alert.significance = constants.SIGNIFICANCE_HIGH
            self.update_alert()
            tendrl_ns.notification_plugin_manager.notify_alert(self.alert)
        except Exception as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Failed to handle the alert of resource %s'
                        ' for node %s' % (
                            alert_obj.resource,
                            alert_obj.node_id,
                        ),
                        "exception": ex
                    }
                )
            )


class AlertHandlerManager(multiprocessing.Process):
    def load_handlers(self):
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            pkg = 'tendrl.alerting.handlers'
            for file_name in os.listdir(path):
                component_path = os.path.join(path, file_name)
                if os.path.isdir(component_path):
                    for py in [f[:-3] for f in os.listdir(component_path)
                               if f.endswith('.py') and f != '__init__.py']:
                        handler_name = '.'.join([pkg, file_name, py])
                        mod = importlib.import_module(handler_name)
                        clsmembers = inspect.getmembers(mod, inspect.isclass)
                        for name, cls in clsmembers:
                            if cls.handles:
                                exec(
                                    "from %s import %s" % (
                                        handler_name,
                                        name
                                    )
                                )
                                self.alert_handlers.append(cls.handles)
        except (SyntaxError, ValueError, ImportError) as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Failed to load the alert handlers.',
                        "exception": ex
                    }
                )
            )
            raise ex

    def __init__(self):
        super(AlertHandlerManager, self).__init__()
        try:
            self.alert_handlers = []
            self.complete = multiprocessing.Event()
            self.load_handlers()
            self.init_alerttypes()
        except (SyntaxError, ValueError, ImportError) as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": 'Alert handler init failed',
                        "exception": ex
                    }
                )
            )
            raise ex

    def init_alerttypes(self):
        for handler in AlertHandler.handlers:
            tendrl_ns.alert_types.append(handler.representive_name)

    def run(self):
        try:
            while not self.complete.is_set():
                new_msg_id = tendrl_ns.alert_queue.get()
                time.sleep(15)
                msg_priority = tendrl_ns.etcd_orm.client.read(
                    '/Messages/%s/priority' % new_msg_id
                ).value
                if msg_priority == 'notice':
                    new_alert_str = tendrl_ns.etcd_orm.client.read(
                        '/Messages/%s/payload' % new_msg_id,
                        recursive=True
                    )._children[0]['value']
                    new_alert = json.loads(new_alert_str)
                    new_alert['alert_id'] = new_msg_id
                    new_alert_obj = AlertUtils().to_obj(new_alert)
                    handled_alert = False
                    for handler in AlertHandler.handlers:
                        if handler.handles == new_alert_obj.resource:
                            handler.handle(new_alert_obj)
                            handled_alert = True
                    if not handled_alert:
                        Event(
                            Message(
                                "error",
                                "alerting",
                                {
                                    "message": 'No alert handler defined for %s and'
                                    '  hence cannot handle alert %s' % (
                                        new_alert_obj.resource,
                                        str(new_alert_obj)
                                    )
                                }
                            )
                        )
                        raise NoHandlerException(
                            'No alert handler defined for %s and hence cannot handle'
                            'alert %s' % (new_alert.resource, str(new_alert))
                        )
        except Exception as ex:
            Event(
                ExceptionMessage(
                    priority="error",
                    publisher="alerting",
                    payload={
                        "message": "Exception caught starting alert handlers.",
                        "exception": ex
                    }
                )
            )

    def stop(self):
        self.complete.set()
