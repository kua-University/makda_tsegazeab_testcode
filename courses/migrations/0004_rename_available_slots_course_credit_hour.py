# Generated by Django 5.1.2 on 2025-01-26 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='available_slots',
            new_name='credit_hour',
        ),
    ]
