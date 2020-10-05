from django import forms
from users.models import KedataUsers

UPGRADE_USER_CHOICES = ['basic', 'advance', 'professional']

class NewUserForm(forms.Form):
    email = forms.EmailField()
    project = forms.CharField()

class UpgradeUserForm(forms.Form):
    email = forms.EmailField()
    add_status = forms.ChoiceField(choices=[('demo', 'demo'), ('basic', 'basic'), ('professional', 'professional')])

    class Meta:
        model = KedataUsers