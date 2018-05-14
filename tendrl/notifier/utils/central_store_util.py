from etcd import EtcdException
from etcd import EtcdKeyNotFound
import json

CLUSTER_ALERT = "cluster"
NODE_ALERT = "node"


def get_alerts():
    alerts_arr = []
    try:
        alerts_arr = NS.tendrl.objects.Alert().load_all()
        notify_only_alerts = \
            NS.tendrl.objects.NotificationOnlyAlert().load_all()
        if notify_only_alerts and len(notify_only_alerts) > 0:
            alerts_arr.extend(notify_only_alerts)
    except EtcdKeyNotFound:
        return alerts_arr
    except (EtcdException, AttributeError) as ex:
        raise ex
    if alerts_arr:
        return alerts_arr
    else:
        return []


def update_alert_delivery(alert):
    alert.delivered = True
    if type(alert) is NS.tendrl.objects.Alert:
        obj = NS.tendrl.objects.Alert(
            alert_id=alert.alert_id
        ).load()
        if alert.severity == obj.severity:
            obj.tags = json.loads(obj.tags)
            obj.delivered = alert.delivered
            obj.save()
            if NODE_ALERT in alert.classification:
                obj = NS.tendrl.objects.NodeAlert(
                    alert_id=alert.alert_id,
                    node_id=alert.node_id
                ).load()
                obj.delivered = alert.delivered
                obj.save()
            if CLUSTER_ALERT in alert.classification:
                obj = NS.tendrl.objects.ClusterAlert(
                    alert_id=alert.alert_id,
                    tags=alert.tags,
                ).load()
                obj.delivered = alert.delivered
                obj.save()
    else:
        # After 10 mins it will deleted
        TTL = 1200
        obj = NS.tendrl.objects.NotificationOnlyAlert(
            alert_id=alert.alert_id,
        ).load()
        obj.delivered = alert.delivered
        obj.save(ttl=TTL)
