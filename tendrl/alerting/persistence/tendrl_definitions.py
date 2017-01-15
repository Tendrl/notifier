from tendrl.commons.etcdobj.etcdobj import EtcdObj
from tendrl.commons.etcdobj import fields


class TendrlDefinitions(EtcdObj):
    """A table of the Os, lazily updated

    """
    __name__ = '/_tendrl/definitions/integrations.d/alerting'

    data = fields.StrField("data")
