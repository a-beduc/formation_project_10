# Generated by Django 5.2b1 on 2025-03-04 09:21

import myauth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(validators=[myauth.validators.validate_age]),
        ),
    ]
