from tendrl.commons import objects


class ClusterAlertCounters(objects.BaseObject):
    def __init__(
        self,
        warn_count=0,
        crit_count=0,
        cluster_id='',
        *args,
        **kwargs
    ):
        super(ClusterAlertCounters, self).__init__(*args, **kwargs)
        self.warning_count = warn_count
        self.critical_count = crit_count
        self.cluster_id = cluster_id
        self.value = '/clusters/{0}/alert_counters'

    def render(self):
        self.value = self.value.format(self.cluster_id)
        return super(ClusterAlertCounters, self).render()
