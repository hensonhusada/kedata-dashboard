# Generated by Django 3.0.8 on 2020-09-10 17:43

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KedataUsers',
            fields=[
                ('user_id', models.CharField(default=users.models.random_string, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=30)),
                ('subscription', models.CharField(max_length=20)),
                ('project_name', models.CharField(max_length=20)),
                ('last_login', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='LastUpdateTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated_user', models.DateTimeField(default='1970-01-01')),
                ('last_updated_user_report', models.DateTimeField(default='1970-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='UsageKeywordMultikey',
            fields=[
                ('keyword_id', models.CharField(default=users.models.random_string, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('media', models.CharField(max_length=30)),
                ('timestamps', models.DateTimeField()),
                ('count', models.IntegerField()),
                ('state', models.CharField(max_length=20)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='multi_keywords', to='users.KedataUsers')),
            ],
        ),
        migrations.CreateModel(
            name='UsageKeywordListening',
            fields=[
                ('keyword_id', models.CharField(default=users.models.random_string, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('text', models.CharField(max_length=40)),
                ('media', models.CharField(max_length=30)),
                ('key_type', models.CharField(max_length=30)),
                ('timestamps', models.DateTimeField()),
                ('count', models.IntegerField()),
                ('state', models.CharField(max_length=20)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listening_keywords', to='users.KedataUsers')),
            ],
        ),
        migrations.CreateModel(
            name='UsageKeywordComparison',
            fields=[
                ('keyword_id', models.CharField(default=users.models.random_string, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('media', models.CharField(max_length=30)),
                ('key_type', models.CharField(max_length=30)),
                ('timestamps', models.DateTimeField()),
                ('count', models.IntegerField()),
                ('state', models.CharField(max_length=20)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comparison_keywords', to='users.KedataUsers')),
            ],
        ),
    ]
