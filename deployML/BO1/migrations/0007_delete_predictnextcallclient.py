# Generated by Django 4.1.13 on 2024-08-21 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BO1', '0006_rename_predictnextcall_predictnextcallclient'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PredictNextCallClient',
        ),
    ]