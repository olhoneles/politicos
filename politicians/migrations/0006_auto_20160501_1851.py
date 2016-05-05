# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0005_auto_20160501_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politician',
            name='cpf',
            field=models.CharField(max_length=11, verbose_name='CPF', db_index=True),
        ),
    ]
