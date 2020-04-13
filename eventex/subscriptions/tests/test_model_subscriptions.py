from datetime import datetime
from unittest import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Luis tavares',
            cpf='12345678901',
            email='luis@tavares.com',
            phone='9208-8183')

        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        '''Subscription must have an auto created_at attr'''
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Luis tavares', str(self.obj))
