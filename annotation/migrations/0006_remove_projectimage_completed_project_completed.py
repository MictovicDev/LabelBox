# Generated by Django 5.1.4 on 2024-12-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0005_projectimage_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimage',
            name='completed',
        ),
        migrations.AddField(
            model_name='project',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]