# Generated by Django 5.0.6 on 2024-06-22 19:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='user_type',
            new_name='roll',
        ),
    ]