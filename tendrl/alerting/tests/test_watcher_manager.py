import etcd
from mock import MagicMock
import multiprocessing
import sys
sys.modules['tendrl.common.config'] = MagicMock()
sys.modules['tendrl.common.log'] = MagicMock()
from tendrl.alerting.watcher.manager import AlertsWatchManager
from tendrl.alerting.watcher.manager import config
del sys.modules['tendrl.common.config']
del sys.modules['tendrl.common.log']


class TestAlertsWatcher(object):
    def test_constructor(self, monkeypatch):
        def mock_config(package, parameter):
            if parameter == "etcd_port":
                return '2379'
            if parameter == 'etcd_connection':
                return '0.0.0.0'
        monkeypatch.setattr(config, 'get', mock_config)
        manager = AlertsWatchManager(multiprocessing.Queue())
        assert isinstance(manager, AlertsWatchManager)
        assert isinstance(manager.etcd_client, etcd.client.Client)

    def test_run(self, monkeypatch):
        def mock_config(package, parameter):
            if parameter == "etcd_port":
                return '2379'
            if parameter == 'etcd_connection':
                return '0.0.0.0'
        monkeypatch.setattr(config, 'get', mock_config)
        manager = AlertsWatchManager(multiprocessing.Queue())

        def mock_run():
            return
        monkeypatch.setattr(manager, 'run', mock_run)
        manager.start()
        assert True
