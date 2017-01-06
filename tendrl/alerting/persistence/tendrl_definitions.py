from tendrl.common.etcdobj.etcdobj import EtcdObj
from tendrl.common.etcdobj import fields


class TendrlDefinitions(EtcdObj):
    """A table of the Os, lazily updated

    """
    __name__ = '/_tendrl/definitions/integrations.d/alerting'

    data = fields.StrField("data")
