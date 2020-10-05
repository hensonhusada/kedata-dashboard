from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from .test_view_home import UserLoggedInSetup
from ..views import users_report_view
from ..models import *

from datetime import datetime

class UserNotLoggedInTests(TestCase):
    def test_redirect(self):
        url = reverse('users:report')
        login_url = reverse('login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class UserLoggedInTests(UserLoggedInSetup):
    def setUp(self):
        super().setUp()

    def test_view_status_code(self):
        url = reverse('users:report')
        print(url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_url_resolve_view(self):
        view = resolve('/users/report/')
        self.assertEquals(view.func, users_report_view)