from etcd import EtcdException
from etcd import EtcdKeyNotFound
from tendrl.commons.objects.cluster_alert import ClusterAlert
from tendrl.commons.objects.node_alert import NodeAlert
from tendrl.commons.objects.notification_only_alert import NotificationOnlyAlert

CLUSTER_ALERT = "cluster"
NODE_ALERT = "node"


def get_alerts():
    alerts_arr = []
    try:
        alerts_arr = NS.tendrl.objects.Alert().load_all()
        alert_notify = NS.tendrl.objects.NotificationOnlyAlert().load_all()
        if alert_notify and len(alert_notify) > 0:
            alerts_arr.extend(alert_notify)
    except EtcdKeyNotFound:
        return alerts_arr
    except (EtcdException, AttributeError) as ex:
        raise ex
    if alerts_arr:
        return alerts_arr
    else:
        return []


def update_alert_delivery(alert):
    alert.delivered = "True"
    if type(alert) is NS.tendrl.objects.Alert:
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
        # update alert
        obj.delivered = alert.delivered
        obj.save()
        alert.save()
    else:
        # After 10 mins it will deleted
        TTL = 600
        obj = NotificationOnlyAlert(
            alert_id=alert.alert_id,
        ).load()
        obj.delivered = alert.delivered
        obj.save(ttl=TTL)
