# Generated by Django 2.1.5 on 2019-11-26 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0006_auto_20191126_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='value',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
