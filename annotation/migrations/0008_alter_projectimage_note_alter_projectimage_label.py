# Generated by Django 5.1.4 on 2024-12-18 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0007_projectimage_note_projectimage_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimage',
            name='Note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='label',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
