from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from .test_view_home import UserLoggedInSetup
from ..views import user_upgrade_view
from ..models import KedataUsers
from ..forms import UpgradeUserForm

from datetime import datetime

class NotLoggedInTests(TestCase):
    def test_redirect(self):
        url = reverse('users:upgrade_user_no_email')
        login_url = reverse('login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class UpgradeUserTestCases(UserLoggedInSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse('users:upgrade_user_no_email')
        self.response = self.client.get(self.url)
        self.ked_user = KedataUsers.objects.create(
                email='henson@doe.com',
                name = 'henson',
                subscription = 'basic',
                project_name = 'endgraf',
                last_login = datetime.now(),
                created_at = datetime.now()
            )

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_view_no_email(self):
        view = resolve('/users/upgrade/')
        self.assertEquals(view.func, user_upgrade_view)

    def test_url_resolve_view_email(self):
        view = resolve('/users/upgrade/henson@doe.com/')
        self.assertEquals(view.func, user_upgrade_view)

    def test_form_has_value_from_url(self):
        email = 'henson@doe.com'
        url = reverse('users:upgrade_user', kwargs={'email': email})
        response = self.client.get(url)
        self.assertContains(response, 'value="henson@doe.com"')