from tendrl.alerting.handlers import AlertHandler


class CpuHandler(AlertHandler):

    handles = 'cpu'
    representive_name = 'cpu_alert'

    def __init__(self):
        AlertHandler.__init__(self)
