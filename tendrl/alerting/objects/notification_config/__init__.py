from tendrl.alerting.objects \
    import AlertingBaseObject
from tendrl.commons.etcdobj import EtcdObj


class NotificationConfig(AlertingBaseObject):
    def __init__(self, config=None, *args, **kwargs):
        super(NotificationConfig, self).__init__(*args, **kwargs)
        self.config = config
        self.value = 'notification_settings/config'
        self._etcd_cls = _NotificationConfig


class _NotificationConfig(EtcdObj):
    __name__ = 'notification_settings'
    _tendrl_cls = NotificationConfig

    def render(self):
        return super(_NotificationConfig, self).render()
