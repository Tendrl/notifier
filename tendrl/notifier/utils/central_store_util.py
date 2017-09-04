from tendrl.commons.objects.alert import Alert
from tendrl.commons.objects.cluster_alert import ClusterAlert
from tendrl.commons.objects.node_alert import NodeAlert
from tendrl.commons.utils import etcd_utils

CLUSTER_ALERT = "cluster"
NODE_ALERT = "node"

def read(key):
    result = {}
    obj = {}
    obj = etcd_utils.read(key)
    if hasattr(obj, 'leaves'):
        for item in obj.leaves:
            if key == item.key:
                result[item.key.split("/")[-1]] = item.value
                return result
            if item.dir is True:
                result[item.key.split("/")[-1]] = read(item.key)
            else:
                result[item.key.split("/")[-1]] = item.value
    return result


def get_alerts():
    alerts_arr = []
    alerts = read('/alerting/alerts')
    for alert_id, alert in alerts.iteritems():
        if alert:
            alerts_arr.append(Alert(**alert))
    return alerts_arr


def update_alert_delivery(alert):
    alert.delivered = "True"
    # update alert
    alert.save()
    if alert.classification == CLUSTER_ALERT:
        # cluster alert
        cluster_alert = read(
            "/alerting/clusters/%s/%s" % (
                alert.tags['integration_id'],
                alert.alert_id
            )
        )
        cluster_alert['delivered'] = alert.delivered
        ClusterAlert(**cluster_alert).save()
    elif alert.classification == NODE_ALERT:
        # node alert
        node_alert = read(
            "/alerting/nodes/%s/%s" % (
                alert.node_id,
                alert.alert_id
            )
        )
        node_alert['delivered'] = alert.delivered
        NodeAlert(**node_alert).save()
