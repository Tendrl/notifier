# flake8: noqa
data = """---
namespace.tendrl.alerting:
  objects:
    Config:
      value: '/_tendrl/config/alerting'
      data:
        help: "The configurations path"
        type: json
      enabled: true
    Alert:
      attrs:
        alert_id:
          help: 'The unique identifier of alert'
          type: String
        node_id:
          help: 'The unique identifier of node on which alert was detected'
          type: String
        time_stamp:
          help: 'The timestamp at which alert was observed'
          type: String
        resource:
          help: 'The resource with problem for which alert was raised'
          type: String
        current_value:
          help: 'The current magnitude(status/utilization) of problem'
          type: String
        tags:
          help: 'Alert specific fields that cannot be generalized for all alerts'
          type: json
        alert_type:
          help: 'The type(status/percentage utilization) of alert'
          type: String
        severity:
          help: 'The severity of alert'
          type: String
        significance:
          help: 'The significance of notifying alert'
          type: String
        ackedby:
          help: 'Entity/person acking the alert'
          type: String
        acked:
          help: 'Indication of whether alert is acked or not'
          type: Boolean
        pid:
          help: 'The id of process raising the alert'
          type: String
        source:
          help: 'The process raising the alert'
          type: String
      enabled: true
      value: alerts/$Alert.alert_id
      list: alerts/
    NotificationMedia:
      attrs:
        name:
          help: 'The name of notification medium'
          type: String
        list: alerting/notification_medium/supported/
tendrl_schema_version: 0.3
"""
