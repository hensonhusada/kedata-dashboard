from django.urls import path, re_path
from . import views as schedule_views

app_name = 'schedule'
urlpatterns = [
    path('', schedule_views.schedule_view, name='schedule'),
    path('list/', schedule_views.ScheduleListView.as_view(), name='schedule_list'),
]