from tendrl.alerting.handlers import AlertHandler


class MemoryHandler(AlertHandler):

    handles = 'memory'
    representive_name = 'memory_alert'

    def __init__(self):
        AlertHandler.__init__(self)
