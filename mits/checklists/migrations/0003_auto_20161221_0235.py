# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0002_checklist_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
