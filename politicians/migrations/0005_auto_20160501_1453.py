# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('politicians', '0004_candidacy_political_party'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='ethnicity',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='mandateeventtype',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='maritalstatus',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='nationality',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='occupation',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='politicaloffice',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='politicianeventtype',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='state',
            name='slug',
        ),
    ]
