# Generated by Django 5.1.6 on 2025-02-26 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_booking_booking_uuid_room_room_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='photo',
            field=models.ImageField(default=1, upload_to='rooms/'),
            preserve_default=False,
        ),
    ]
