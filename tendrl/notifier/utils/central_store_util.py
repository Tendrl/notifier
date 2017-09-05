from tendrl.commons.objects.alert import Alert
from tendrl.commons.objects.cluster_alert import ClusterAlert
from tendrl.commons.objects.node_alert import NodeAlert
from tendrl.commons.utils import etcd_utils

CLUSTER_ALERT = "cluster"
NODE_ALERT = "node"


def get_alerts():
    alerts_arr = []
    try:
        alerts_arr = NS.tendrl.objects.Alert().load_all()
    except EtcdKeyNotFound:
        return alerts_arr
    except (EtcdException, AttributeError) as ex:
        raise ex
    if alerts_arr:
        return alerts_arr
    else:
        return []


def update_alert_delivery(alert):
    if alert.classification == NODE_ALERT:
        obj = NodeAlert(
            alert_id=alert.alert_id,
            node_id=alert.node_id
        ).load()
    elif alert.classification == CLUSTER_ALERT:
        obj = ClusterAlert(
            alert_id=alert.alert_id,
            tags=alert.tags,
        ).load()
    alert.delivered = "True"
    # update alert
    obj.delivered = alert.delivered
    obj.save()
    alert.save()
