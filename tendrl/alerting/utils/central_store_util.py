from tendrl.alerting.objects.alert import Alert
from tendrl.alerting.objects.alert import AlertUtils
from tendrl.alerting.objects.alert_types import AlertTypes


# this function can return json for any etcd key
def read(key):
    result = {}
    job = NS._int.client.read(key)
    if hasattr(job, 'leaves'):
        for item in job.leaves:
            if item.dir is True:
                result[item.key.split("/")[-1]] = read(item.key)
            else:
                result[item.key.split("/")[-1]] = item.value
    return result


def get_event_ids():
    event_ids = []
    etcd_events = NS._int.client.read(
        '/messages/events'
    )
    for event in etcd_events.leaves:
        event_parts = event.key.split('/')
        if len(event_parts) >= 4:
            event_ids.append(event_parts[3])
    return event_ids


def get_alert_types():
    return AlertTypes().load()


def get_alert(alert_id):
    return Alert(alert_id).load()


def get_alerts():
    # TODO: Revert to using object#load instead of etcd read
    # once the issue in object#load is found and fixed.
    alerts_arr = []
    alerts = read('/alerting/alerts')
    for alert_id, alert in alerts.iteritems():
        alerts_arr.append(AlertUtils().to_obj(alert))
    return alerts_arr
