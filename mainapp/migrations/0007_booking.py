# Generated by Django 2.2.12 on 2021-03-25 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_userregistration_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='file/')),
                ('boked', models.BooleanField(default=False)),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.OwnerDetails')),
                ('prop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ListingModel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserRegistration')),
            ],
        ),
    ]
