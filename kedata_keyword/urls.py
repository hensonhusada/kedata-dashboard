from django.urls import path, re_path
from . import views as keyword_views

app_name = 'keyword'
urlpatterns = [
    path('report/', keyword_views.homeview, name='report'),    
    path('state/', keyword_views.stateview, name='state'),
    path('state/<type>/<key_id>', keyword_views.stateview, name='state_with_key'),
    path('keywords/<user_id>', keyword_views.users_keyword_view, name='keyword'),
    path('issue/', keyword_views.create_issue_view, name='create_issue'),
    path('issue/<type>/<key_id>', keyword_views.create_issue_view, name='create_issue_with_key')
]