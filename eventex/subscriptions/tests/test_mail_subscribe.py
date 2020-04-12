from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Luis tavares', cpf='12345678901',
                    email='luis@tavares.com', phone='21-99618-6180')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        '''Email subject must be ‘Confirmação de inscrição’'''
        expect = 'Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        '''Email must be from contato@eventex.com'''
        expect = 'contato@eventex.com'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        '''Email must be sent to the user and to the sender'''
        expect = ['contato@eventex.com', 'luis@tavares.com']
        self.assertEqual(expect, self.email.to)


    def test_subscription_email_body(self):
        contents = [
            'Luis tavares',
            '12345678901',
            'luis@tavares.com',
            '21-99618-6180',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)