# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0003_auto_20160423_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidacy',
            name='political_party',
            field=models.ForeignKey(blank=True, to='politicians.PoliticalParty', null=True),
        ),
    ]
