# Generated by Django 3.1.1 on 2020-10-21 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0036_auto_20201009_0614'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='contact_email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='contact_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='contact_content',
            new_name='query',
        ),
    ]
