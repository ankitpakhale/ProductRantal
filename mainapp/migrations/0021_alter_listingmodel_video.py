# Generated by Django 4.0.2 on 2022-03-25 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0020_alter_listingmodel_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingmodel',
            name='video',
            field=models.FileField(blank=True, default='', null=True, upload_to='video/'),
        ),
    ]
