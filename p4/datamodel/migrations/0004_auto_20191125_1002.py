# Generated by Django 2.1.5 on 2019-11-25 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0003_counter_counter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counter',
            old_name='counter',
            new_name='value',
        ),
    ]