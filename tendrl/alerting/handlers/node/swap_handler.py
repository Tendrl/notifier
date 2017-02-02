from tendrl.alerting.handlers import AlertHandler


class SwapHandler(AlertHandler):

    handles = 'swap'
    representive_name = 'swap_alert'

    def __init__(self):
        AlertHandler.__init__(self)
