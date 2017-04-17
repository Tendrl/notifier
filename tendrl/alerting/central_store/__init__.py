from tendrl.alerting.objects.alert import Alert
from tendrl.alerting.objects.alert import AlertUtils
from tendrl.alerting.objects.alert_types import AlertTypes
from tendrl.alerting.utils import read as etcd_read
from tendrl.commons import central_store


class AlertingEtcdPersister(central_store.EtcdCentralStore):
    def __init__(self):
        super(AlertingEtcdPersister, self).__init__()

    def get_event_ids(self):
        event_ids = []
        etcd_events = NS.etcd_orm.client.read(
            '/messages/events'
        )
        for event in etcd_events.leaves:
            event_parts = event.key.split('/')
            if len(event_parts) >= 4:
                event_ids.append(event_parts[3])
        return event_ids

    def save_config(self, config):
        NS.etcd_orm.save(config)

    def save_definition(self, definition):
        NS.etcd_orm.save(definition)

    def get_alert_types(self):
        return AlertTypes().load()

    def get_alert(self, alert_id):
        return Alert(alert_id).load()

    def get_alerts(self):
        # TODO: Revert to using object#load instead of etcd read
        # once the issue in object#load is found and fixed.
        alerts_arr = []
        alerts = etcd_read('/alerting/alerts')
        for alert_id, alert in alerts.iteritems():
            alerts_arr.append(AlertUtils().to_obj(alert))
        return alerts_arr

    def save_alert(self, alert):
        NS.etcd_orm.save(alert)

    def save_nodealert(self, node_alert):
        NS.etcd_orm.save(node_alert)

    def save_notificationmedia(self, notification_media):
        NS.etcd_orm.save(notification_media)

    def save_alerttypes(self, alert_types):
        NS.etcd_orm.save(alert_types)

    def save_notificationconfigfield(self, notification_config_field):
        NS.etcd_orm.save(notification_config_field)

    def save_notificationconfig(self, notification_config):
        NS.etcd_orm.save(notification_config)

    def save_clusteralert(self, cluster_alert):
        NS.etcd_orm.save(cluster_alert)
