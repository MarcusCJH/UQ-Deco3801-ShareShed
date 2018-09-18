# Generated by Django 2.1 on 2018-09-10 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user_id',
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]