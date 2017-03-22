try:
    from gevent import monkey
except ImportError:
    pass
else:
    monkey.patch_all()

from tendrl.commons import TendrlNS


class AlertingNS(TendrlNS):
    def __init__(
        self,
        ns_name='alerting',
        ns_src='tendrl.alerting'
    ):
        super(AlertingNS, self).__init__(ns_name, ns_src)
