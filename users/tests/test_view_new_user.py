from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from .test_view_home import UserLoggedInSetup
from ..views import HomeView, NewUserView
from ..models import KedataUsers
from ..forms import NewUserForm

class NotLoggedInTests(TestCase):
    def test_redirect(self):
        url = reverse('users:new_user')
        login_url = reverse('login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class NewUserTestCases(UserLoggedInSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse('users:new_user')
        self.response = self.client.get(self.url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolve_view(self):
        view = resolve('/users/new/')
        self.assertEquals(view.func.view_class, NewUserView)
