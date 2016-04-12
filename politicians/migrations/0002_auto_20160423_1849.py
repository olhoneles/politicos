# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidacy',
            name='politician',
            field=models.ForeignKey(related_name='candidacies', to='politicians.Politician'),
        ),
    ]
