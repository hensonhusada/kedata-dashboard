from django.urls import path, re_path
from . import views as users_views

app_name = 'users'
urlpatterns = [
    path('', users_views.HomeView.as_view(), name='home'),
    path('new/', users_views.NewUserView.as_view(), name='new_user'),
    path('upgrade/', users_views.user_upgrade_view, name='upgrade_user_no_email'),
    path('upgrade/<email>/', users_views.user_upgrade_view, name='upgrade_user'),
    # path('report/', users_views.users_report_view, name='report'),
    
]

