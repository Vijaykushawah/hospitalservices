# Generated by Django 3.1.1 on 2020-10-05 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0031_requestsforapproval_userbiodataid'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestsforapproval',
            name='request_type',
            field=models.CharField(choices=[('contact', 'Contact'), ('connect', 'Connect'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
    ]