# Generated by Django 5.1.6 on 2025-02-27 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_amenity_room_area_room_max_guest_room_amenities'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
