from tendrl.alerting.handlers import AlertHandler


class MountPointHandler(AlertHandler):

    handles = 'df'
    representive_name = 'mount_point_alert'

    def __init__(self):
        AlertHandler.__init__(self)
