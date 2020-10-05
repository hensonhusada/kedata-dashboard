from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

# Create your tests here.
from ..views import HomeView
from ..models import KedataUsers

from datetime import datetime

class UserLoggedInSetup(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='john@doe.com',
            )
        self.client.login(username=self.username, password=self.password)

class UserNotLoggedInTests(TestCase):
    def test_redirect(self):
        url = reverse('users:home')
        login_url = reverse('login')
        self.response = self.client.get(url)
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=url))

class UsersLoggedInHomeTests(UserLoggedInSetup):
    def setUp(self):
        super().setUp()        
        self.ked_user = KedataUsers.objects.create(
                email='henson@doe.com',
                name = 'henson',
                subscription = 'basic',
                project_name = 'endgraf',
                last_login = datetime.now(),
                created_at = datetime.now()
            )        
        url = reverse('users:home')
        self.response = self.client.get(url)

    def test_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/users/')
        self.assertEquals(view.func.view_class, HomeView)

    def test_view_contain_url_to_upgrade_user(self):
        self.assertContains(self.response, reverse('users:upgrade_user', kwargs={'email': 'henson@doe.com'}))