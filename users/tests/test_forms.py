from django.test import TestCase
from ..forms import NewUserForm, UpgradeUserForm

class FormsTests(TestCase):
    def test_new_user_form_has_fields(self):
        form = NewUserForm()
        expected = ['email', 'project']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_upgrade_user_form_has_fields(self):
        form = UpgradeUserForm()
        expected = ['email', 'add_status']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)