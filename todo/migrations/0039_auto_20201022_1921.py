# Generated by Django 3.1.1 on 2020-10-22 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0038_appointment_doctor_patient_patientdischargedetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='todo/images/'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='todo/images/'),
        ),
    ]
