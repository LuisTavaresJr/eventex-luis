import hashlib

from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')
    def test_get(self):
        '''Get /inscricao/ must return status code 200'''
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        '''Must use template subscriptions / subscription_form.html'''
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html Must contain input tags"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        '''Html must contain csrf'''
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        '''Context must have subscription form'''
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    

class SubscribePostValid(TestCase):
    def setUp(self):
        self.data = dict(name='Luis tavares', cpf='12345678901',
                    email='luis@tavares.com', phone='21-99618-6180')
        self.response = self.client.post('/inscricao/', self.data)

    def test_post(self):
        '''Valid POST should redirect to /inscricao/{hash_obj.hexdigest()}/'''
        hash_obj = hashlib.md5(self.data['email'].encode())
        self.assertRedirects(self.response, f'/inscricao/{hash_obj.hexdigest()}/')

    def test_send_subscribe_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})
    def test_post(self):
        '''Invalid POST should not redirect'''
        self.assertEqual(200, self.response.status_code)
    def test_template(self):
      self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())

