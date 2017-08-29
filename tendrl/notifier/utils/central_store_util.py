from tendrl.commons.objects.alert import Alert
from tendrl.commons.objects.cluster_alert import ClusterAlert
from tendrl.commons.objects.node_alert import NodeAlert
from tendrl.commons.utils import etcd_utils


def read(key):
    result = {}
    job = {}
    job = etcd_utils.read(key)
    if hasattr(job, 'leaves'):
        for item in job.leaves:
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
        alerts_arr.append(Alert(**alert))
    return alerts_arr


def update_alert_delivery(alert):
    alert.delivered = "True"
    # update alert
    alert.save()
    if "alert_catagory" in alert.tags:
        if alert.tags['alert_catagory'] == 'cluster':
            # cluster alert
            cluster_alert = read(
                "/alerting/clusters/%s/%s" % (
                    alert.tags['integration_id'],
                    alert.alert_id
                )
            )
            cluster_alert['delivered'] = alert.delivered
            ClusterAlert(**cluster_alert).save()
        elif alert.tags['alert_catagory'] == 'node':
            # node alert
            node_alert = read(
                "/alerting/nodes/%s/%s" % (
                    alert.node_id,
                    alert.alert_id
                )
            )
            node_alert['delivered'] = alert.delivered
            NodeAlert(**node_alert).save()
