from django.db import models

import uuid

# Create your models here.
class ScheduleList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    media = models.CharField(max_length=20)
    date = models.DateTimeField()
    state = models.CharField(max_length=10)
    response = models.CharField(max_length=10, default='OK')