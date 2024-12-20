# Generated by Django 5.1.4 on 2024-12-18 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_alter_projectimage_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimage',
            name='Note',
        ),
        migrations.RemoveField(
            model_name='projectimage',
            name='label',
        ),
        migrations.CreateModel(
            name='AnnotatdImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=500)),
                ('Note', models.TextField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='annotation.project')),
            ],
        ),
    ]
