from django import forms

class ScheduleForm(forms.Form):
    media = forms.ChoiceField(choices=[
        ('twitter', 'twitter'),
        ('instagram', 'instagram'),
        ('news', 'news')
        ])
