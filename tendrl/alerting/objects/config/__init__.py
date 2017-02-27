from tendrl.commons.etcdobj import EtcdObj
from tendrl.commons import config as cmn_config
from tendrl.alerting.objects \
    import AlertingBaseObject


class Config(AlertingBaseObject):
    def __init__(self, config=None, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        self.value = '_tendrl/config/alerting/data'
        if config is None:
            config = cmn_config.load_config(
                'alerting',
                "/etc/tendrl/alerting/alerting.conf.yaml"
            )
        self.data = config
        self._etcd_cls = _ConfigEtcd


class _ConfigEtcd(EtcdObj):
    """Config etcd object, lazily updated

    """
    __name__ = '_tendrl/config/alerting'
    _tendrl_cls = Config
