# Generated by Django 4.0.5 on 2022-06-26 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum_body', '0005_message_discuss'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='Messages',
        ),
    ]