from django import forms

class KeywordStateForm(forms.Form):
    fields = forms.ChoiceField(choices=[('listening', 'listening'), ('comparison', 'comparison'), ('multi', 'multi')])
    keyword_id = forms.CharField()
    status = forms.ChoiceField(choices=[('waiting', 'waiting'), ('done', 'done'), ('fail', 'fail')])

class CreateIssueForm(forms.Form):
    fields = forms.ChoiceField(choices=[('listening', 'listening'), ('comparison', 'comparison'), ('multi', 'multi')])
    keyword_id = forms.CharField()
    email = forms.ChoiceField(choices=[('henzonlol@gmail.com', 'henzonlol@gmail.com'),('naruto@doe.com', 'naruto@doe.com')])