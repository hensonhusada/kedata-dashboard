# Generated by Django 3.0.8 on 2020-09-14 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lastupdatetime',
            old_name='last_updated_user_report',
            new_name='last_updated_keyword',
        ),
    ]
