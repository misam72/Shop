# Generated by Django 4.2.6 on 2023-10-24 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
