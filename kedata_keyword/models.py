from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import user_logged_in, user_logged_out

import random


# Create your models here.
class LogKeywordCount(models.Model):
    update_time = models.DateTimeField()
    json_data_media = models.CharField(max_length=200)
    json_data_name = models.CharField(max_length=200)