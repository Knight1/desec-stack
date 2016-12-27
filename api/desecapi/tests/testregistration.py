from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .utils import utils
from desecapi import models
from datetime import timedelta
from django.utils import timezone
from django.core import mail
from desecapi.emails import send_account_lock_email
from desecapi import settings


class RegistrationTest(APITestCase):

    def test_registration_successful(self):
        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.7")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.7")

    def test_multiple_registration_captcha_required_same_ip_short_time(self):
        outboxlen = len(mail.outbox)

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.7")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.7")
        self.assertEqual(user.captcha_required, False)

        self.assertEqual(len(mail.outbox), outboxlen)

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.7")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.7")
        self.assertEqual(user.captcha_required, True)

        self.assertEqual(len(mail.outbox), outboxlen + 1)

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.7")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.7")
        self.assertEqual(user.captcha_required, True)

        self.assertEqual(len(mail.outbox), outboxlen + 2)

    def test_multiple_registration_no_captcha_required_different_ip(self):
        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.8")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.8")
        self.assertEqual(user.captcha_required, False)

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.9")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.9")
        self.assertEqual(user.captcha_required, False)

    def test_multiple_registration_no_captcha_required_same_ip_long_time(self):
        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.10")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.10")
        self.assertEqual(user.captcha_required, False)

        #fake registration time
        user.created = timezone.now() - timedelta(hours=settings.ABUSE_LOCK_ACCOUNT_BY_REGISTRATION_IP_PERIOD_HRS+1)
        user.save()

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.10")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.registration_remote_ip, "1.3.3.10")
        self.assertEqual(user.captcha_required, False)

    def test_send_captcha_email_manually(self):
        outboxlen = len(mail.outbox)

        url = reverse('register')
        data = {'email': utils.generateUsername(), 'password': utils.generateRandomString(size=12)}
        response = self.client.post(url, data, REMOTE_ADDR="1.3.3.10")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data['email'])
        send_account_lock_email(None, user)

        self.assertEqual(len(mail.outbox), outboxlen+1)