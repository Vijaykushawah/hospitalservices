# Generated by Django 3.1.1 on 2020-10-03 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0015_auto_20201003_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybiodata',
            name='body_Type',
            field=models.CharField(choices=[('Slim', 'Slim'), ('Average', 'Average'), ('Fit', 'Fit'), ('Healthy', 'Healthy'), ('Chubby', 'Chubby'), ('Fatty', 'Fatty'), ('Not_Specified', 'Not Specified')], default='Average', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='cast',
            field=models.CharField(choices=[('Kushwaha', 'Kushwaha'), ('Maurya', 'Maurya'), ('Shakya', 'Shakya'), ('Saini', 'Saini'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='complexion',
            field=models.CharField(choices=[('Fair', 'Fair'), ('Milky_Fair', 'Milky Fair'), ('Very_Fair', 'Very Fair'), ('Brown', 'Brown'), ('Dark', 'Dark'), ('Normal', 'Normal'), ('Not_Specified', 'Not Specified')], default='Fair', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='contact_privacy',
            field=models.CharField(choices=[('Visible_To_All', 'Visible To All'), ('Visible_To_me', 'Visible To Me'), ('Hidden', 'Hidden'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='created_by',
            field=models.CharField(choices=[('_Self', ' Self'), ('Parents', 'Parents'), ('Friedns', 'Friedns'), ('Relatives', 'Relatives'), ('Others', 'Others'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='diet',
            field=models.CharField(choices=[('Vegitarian', 'Vegitarian'), ('Non_Vegetaria', 'Non Vegetaria'), ('Eagitarian', 'Eagitarian'), ('Not_Specified', 'Not Specified')], default='Vegitarian', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='father_occupation',
            field=models.CharField(choices=[('Accountant', 'Accountant'), ('Teacher', 'Teacher'), ('Technician', 'Technician'), ('Laborer', 'Laborer'), ('Banker', 'Banker'), ('Farmer', 'Farmer'), ('Shop_Keeper', 'Shop Keeper'), ('Business_Man', 'Business Man'), ('Engineer', 'Engineer'), ('Doctor', 'Doctor'), ('others', 'Others'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='gender',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='manglik',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='marital_Status',
            field=models.CharField(choices=[('married', 'Married'), ('Not_married', 'Not Married'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='mother_Toung',
            field=models.CharField(choices=[('Hindi', 'Hindi'), ('English', 'English'), ('Both', 'Both'), ('Not_Specified', 'Not Specified')], default='Hindi', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='mother_occupation',
            field=models.CharField(choices=[('House_wife', 'House Wife'), ('Accountant', 'Accountant'), ('Teacher', 'Teacher'), ('Technician', 'Technician'), ('Laborer', 'Laborer'), ('Banker', 'Banker'), ('Farmer', 'Farmer'), ('Shop_Keeper', 'Shop Keeper'), ('Business_Man', 'Business Man'), ('Engineer', 'Engineer'), ('Doctor', 'Doctor'), ('others', 'Others'), ('Not_Specified', 'Not Specified')], default='House_wife', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='physical_disability',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='profession',
            field=models.CharField(choices=[('Accountant', 'Accountant'), ('Teacher', 'Teacher'), ('Technician', 'Technician'), ('Laborer', 'Laborer'), ('Banker', 'Banker'), ('Farmer', 'Farmer'), ('Shop_Keeper', 'Shop Keeper'), ('Business_Man', 'Business Man'), ('Engineer', 'Engineer'), ('Doctor', 'Doctor'), ('others', 'Others'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='profession_type',
            field=models.CharField(choices=[('Private', 'Private'), ('Government', 'Government'), ('Semi_Govt', 'Semi Govt'), ('Contratual', 'Contratual'), ('Others', 'Others'), ('Not_Specified', 'Not Specified')], default='Not_Specified', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='religion',
            field=models.CharField(choices=[('Hindu', 'Hindu'), ('Muslim', 'Muslim'), ('Sikh', 'Sikh'), ('Parsi', 'Parsi'), ('Not_Specified', 'Not Specified')], default='Hindu', max_length=20),
        ),
        migrations.AlterField(
            model_name='mybiodata',
            name='social',
            field=models.CharField(choices=[('Religious_Background', 'Religious Background'), ('Normal', 'Normal'), ('Both', 'Both'), ('Not_Specified', 'Not Specified')], default='Religious_Background', max_length=20),
        ),
    ]
