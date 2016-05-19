# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0006_auto_20160501_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electionround',
            name='round_number',
            field=models.CharField(max_length=1, verbose_name='Round', choices=[(1, 'Round 1'), (2, 'Round 2')]),
        ),
    ]
