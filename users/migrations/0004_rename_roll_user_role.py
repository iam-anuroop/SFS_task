# Generated by Django 5.0.6 on 2024-06-22 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_user_type_user_roll'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='roll',
            new_name='role',
        ),
    ]