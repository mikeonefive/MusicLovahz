# Generated by Django 5.1.3 on 2025-03-04 14:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiclovahz', '0004_user_matches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='matches',
            field=models.ManyToManyField(blank=True, related_name='matched_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='users', to='musiclovahz.song'),
        ),
    ]
