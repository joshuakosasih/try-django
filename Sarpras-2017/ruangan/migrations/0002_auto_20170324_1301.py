# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruangan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ruangan',
            name='tipe',
            field=models.CharField(choices=[('Ruang', 'Ruang'), ('Selasar', 'Selasar'), ('Lapangan', 'Lapangan')], default='Selasar', max_length=50),
        ),
    ]
