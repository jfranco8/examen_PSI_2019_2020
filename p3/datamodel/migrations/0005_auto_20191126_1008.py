# Generated by Django 2.1.5 on 2019-11-26 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0004_auto_20191125_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='value',
            field=models.IntegerField(default=0),
        ),
    ]
