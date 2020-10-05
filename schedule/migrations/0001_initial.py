# Generated by Django 3.0.8 on 2020-09-30 14:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleList',
            fields=[
                ('id', models.UUIDField(default=uuid.UUID('e819adbe-d994-4ec2-89a9-524773e22476'), editable=False, primary_key=True, serialize=False)),
                ('media', models.CharField(max_length=20)),
                ('date', models.DateTimeField()),
                ('state', models.CharField(max_length=10)),
                ('response', models.CharField(max_length=10)),
            ],
        ),
    ]
