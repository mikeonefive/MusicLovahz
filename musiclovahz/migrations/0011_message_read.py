# Generated by Django 5.1.3 on 2025-03-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musiclovahz', '0010_remove_message_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
