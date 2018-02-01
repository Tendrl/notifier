import __builtin__
import etcd
from etcd import Client
import maps
from mock import patch

import tendrl.commons.objects.node_context as node


class TestCase(object):
    @patch.object(etcd, "Client")
    @patch.object(Client, "read")
    @patch.object(Client, "write")
    @patch.object(node.NodeContext, '_get_node_id')
    def init(self, patch_get_node_id, patch_write, patch_read, patch_client):
        patch_get_node_id.return_value = 1
        patch_read.return_value = etcd.Client()
        patch_write.return_value = etcd.Client()
        patch_client.return_value = etcd.Client()
        setattr(__builtin__, "NS", maps.NamedDict())
        setattr(NS, "_int", maps.NamedDict())
        NS._int.etcd_kwargs = {
            'port': 1,
            'host': 2,
            'allow_reconnect': True}
        NS._int.client = etcd.Client(**NS._int.etcd_kwargs)
        NS._int.wclient = etcd.Client(**NS._int.etcd_kwargs)
        NS["config"] = maps.NamedDict()
        NS.config["data"] = maps.NamedDict()
        NS.config.data['tags'] = "test"
        NS["notifier"] = maps.NamedDict()
