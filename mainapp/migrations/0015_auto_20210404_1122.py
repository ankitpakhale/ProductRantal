# Generated by Django 2.2.12 on 2021-04-04 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20210404_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownerdetails',
            name='Plan',
            field=models.CharField(max_length=20),
        ),
    ]
