# Generated by Django 5.0.6 on 2024-09-27 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_managers'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]
