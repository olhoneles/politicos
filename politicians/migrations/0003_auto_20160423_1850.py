# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0002_auto_20160423_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politician',
            name='gender',
            field=models.CharField(choices=[(b'F', 'Female'), (b'M', 'Male'), (b'N', 'Uninformed')], max_length=1, blank=True, null=True, verbose_name='Gender', db_index=True),
        ),
    ]
