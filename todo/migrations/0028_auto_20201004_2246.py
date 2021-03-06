# Generated by Django 3.1.1 on 2020-10-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0027_biodatahelp'),
    ]

    operations = [
        migrations.AddField(
            model_name='biodatahelp',
            name='contact_number',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='biodatahelp',
            name='email_id',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='biodatahelp',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='biodatahelp',
            name='subject',
            field=models.CharField(default='', max_length=100),
        ),
    ]
