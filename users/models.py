from django.db import models
from django.contrib.auth.models import User

from bulk_update_or_create import BulkUpdateOrCreateQuerySet
import random

def random_string():
    return str(random.randint(10000, 99999))
    
# Create your models here.
class KedataUsers(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    user_id = models.CharField(unique=True, default=random_string, max_length=50, primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    subscription = models.CharField(max_length=20)
    project_name = models.CharField(max_length=20)
    last_login = models.DateTimeField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.email

class UsageKeywordListening(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    keyword_id = models.CharField(unique=True, default=random_string, max_length=26, primary_key=True)
    text = models.CharField(max_length=40)
    media = models.CharField(max_length=30)
    key_type = models.CharField(max_length=30)
    timestamps = models.DateTimeField()
    count = models.IntegerField()
    state = models.CharField(max_length=20)
    user_id = models.ForeignKey(KedataUsers, on_delete=models.CASCADE, related_name='listening_keywords')

    def __str__(self):
        return self.text

class UsageKeywordComparison(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    keyword_id = models.CharField(unique=True, default=random_string, max_length=26, primary_key=True)
    name = models.CharField(max_length=40)
    media = models.CharField(max_length=30)
    key_type = models.CharField(max_length=30)
    timestamps = models.DateTimeField()
    count = models.IntegerField()
    state = models.CharField(max_length=20)
    user_id = models.ForeignKey(KedataUsers, on_delete=models.CASCADE, related_name='comparison_keywords')

    def __str__(self):
        return self.name

class UsageKeywordMultikey(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    keyword_id = models.CharField(unique=True, default=random_string, max_length=26, primary_key=True)
    name = models.CharField(max_length=40)
    media = models.CharField(max_length=30)
    timestamps = models.DateTimeField()
    count = models.IntegerField()
    state = models.CharField(max_length=20)
    user_id = models.ForeignKey(KedataUsers, on_delete=models.CASCADE, related_name='multi_keywords')

    def __str__(self):
        return self.name

class LastUpdateTime(models.Model):
    last_updated_user = models.DateTimeField(default='1970-01-01')
    last_updated_keyword = models.DateTimeField(default='1970-01-01')
