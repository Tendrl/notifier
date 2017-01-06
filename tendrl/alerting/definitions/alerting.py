# flake8: noqa
data = """---
namespace.tendrl.alerting:
  objects:
    Config:
      value: '/_tendrl/config/alerting'
      data:
        help: "The configurations path"
        type: json
    Alert:
      attrs:
        alert_id:
          type: String
        node_id:
          type: String
        time_stamp:
          type: String
        resource:
          type: String
        current_value:
          type: String
        tags:
          type: json
        alert_type:
          type: String
        severity:
          type: String
        significance:
          type: String
        ackedby:
          type: String
        acked:
          type: Boolean
        pid:
          type: String
        source:
          type: String
      enabled: true
      value: alerts/$Alert.alert_id
      list: alerts/
    NotificationMedia:
      attrs:
        name:
          type: String
        list: alerting/notification_medium/supported/
tendrl_schema_version: 0.3
"""
