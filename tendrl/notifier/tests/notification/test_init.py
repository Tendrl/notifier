import etcd
from etcd import Client
import mock
from mock import MagicMock
from mock import patch
import pytest

from tendrl.commons.objects.alert import Alert
from tendrl.notifier import notification
from tendrl.notifier.tests import TestCase


class TestNotification(TestCase):
    flag = True

    def is_set(self):
        TestNotification.flag = not TestNotification.flag
        return TestNotification.flag

    @mock.patch('tendrl.commons.event.Event.__init__',
                mock.Mock(return_value=None))
    @mock.patch('tendrl.commons.message.Message.__init__',
                mock.Mock(return_value=None))
    @mock.patch('tendrl.commons.objects.BaseObject.__init__',
                mock.Mock(return_value=True))
    @mock.patch('tendrl.commons.objects.BaseObject.save',
                mock.Mock(return_value=True))
    @patch.object(etcd, "Client")
    @patch.object(Client, "read")
    def test_init(self, patch_read, patch_etcd):
        patch_etcd.return_value = etcd.Client()
        patch_read.return_value = etcd.Client()
        self.init()
        with patch.object(
            notification, 'list_modules_in_package_path'
        ) as list_module:
            list_module.return_value = [
                ('test_mail_handler',
                 'tendrl.notifier.tests.notification.'
                 'handlers.test_mail_handler'
                 ),
                ('test_snmp_handler',
                 'tendrl.notifier.tests.notification.'
                 'handlers.test_snmp_handler'
                 )
            ]
            notification.NotificationPluginManager()
        with patch.object(
            notification, 'list_modules_in_package_path'
        ) as list_module:
            list_module.return_value = [
                ('test_mail_handler_error',
                 'tendrl.notifier.tests.notification.'
                 'handlers.test_mail_handler_error'
                 )
            ]
            with pytest.raises(ImportError):
                notification.NotificationPluginManager()

    @mock.patch('tendrl.commons.event.Event.__init__',
                mock.Mock(return_value=None))
    @mock.patch('tendrl.commons.message.Message.__init__',
                mock.Mock(return_value=None))
    @mock.patch('tendrl.commons.objects.BaseObject.__init__',
                mock.Mock(return_value=True))
    @mock.patch('tendrl.commons.objects.BaseObject.save',
                mock.Mock(return_value=True))
    @mock.patch('tendrl.commons.objects.BaseObject.load',
                mock.Mock(return_value=Alert))
    @patch.object(etcd, "Client")
    @patch.object(Client, "read")
    def test_run(self, patch_read, patch_etcd):
        patch_etcd.return_value = etcd.Client()
        patch_read.return_value = etcd.Client()
        self.init()
        with patch.object(
            notification, 'list_modules_in_package_path'
        ) as list_module:
            list_module.return_value = [
                ('test_mail_handler',
                 'tendrl.notifier.tests.notification.'
                 'handlers.test_mail_handler'
                 ),
                ('test_snmp_handler',
                 'tendrl.notifier.tests.notification.'
                 'handlers.test_snmp_handler'
                 )
            ]
            obj = notification.NotificationPluginManager()
            with patch.object(
                notification, 'get_alerts'
            ) as alerts:
                alerts.return_value = [Alert(
                    alert_id="1",
                    node_id="2",
                    resource="test_alert",
                    alert_type="status",
                    severity="warning",
                    classification="testing",
                    delivered="False",
                    tags='{}'
                )]
                with patch.object(
                    obj.complete, 'is_set', self.is_set
                ):
                    with patch.object(
                        etcd.Lock, 'acquire'
                    ) as mock_acquire:
                        mock_acquire.return_value = True
                        with patch.object(
                            etcd.Lock, 'is_acquired'
                        ) as mock_is_acq:
                            mock_is_acq.return_value = True
                            with patch.object(
                                etcd.Lock, 'release'
                            ) as mock_rel:
                                mock_rel.return_value = True
                                NS.tendrl = MagicMock()
                                obj.run()
