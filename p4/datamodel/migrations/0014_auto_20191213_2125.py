# Generated by Django 2.1.5 on 2019-12-13 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0013_auto_20191213_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='cat1',
        ),
        migrations.RemoveField(
            model_name='move',
            name='cat2',
        ),
        migrations.RemoveField(
            model_name='move',
            name='cat3',
        ),
        migrations.RemoveField(
            model_name='move',
            name='cat4',
        ),
        migrations.RemoveField(
            model_name='move',
            name='mouse',
        ),
    ]
