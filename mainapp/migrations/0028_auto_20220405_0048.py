# Generated by Django 3.0 on 2022-04-04 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0027_auto_20220405_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listingmodel',
            name='builtin_wardrobe',
        ),
        migrations.RemoveField(
            model_name='listingmodel',
            name='dish_washer',
        ),
        migrations.RemoveField(
            model_name='listingmodel',
            name='fencing',
        ),
        migrations.RemoveField(
            model_name='listingmodel',
            name='floor_covering',
        ),
        migrations.RemoveField(
            model_name='listingmodel',
            name='internet',
        ),
        migrations.RemoveField(
            model_name='listingmodel',
            name='medical',
        ),
    ]
