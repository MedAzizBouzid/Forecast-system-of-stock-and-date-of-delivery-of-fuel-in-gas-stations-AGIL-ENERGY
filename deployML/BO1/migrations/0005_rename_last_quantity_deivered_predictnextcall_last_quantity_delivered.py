# Generated by Django 4.1.13 on 2024-08-21 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BO1', '0004_predictnextcall'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predictnextcall',
            old_name='last_quantity_deivered',
            new_name='last_quantity_delivered',
        ),
    ]