# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidacy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('elected', models.BooleanField(verbose_name='Elected')),
            ],
            options={
                'ordering': ['election_round__election__year', 'election_round', 'politician__name'],
                'verbose_name': 'Candidacy',
                'verbose_name_plural': 'Candidacies',
            },
        ),
        migrations.CreateModel(
            name='CandidacyStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Candidacy Status',
                'verbose_name_plural': 'Candidacies Status',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('logo', models.URLField(null=True, verbose_name='Logo', blank=True)),
            ],
            options={
                'ordering': ['state', 'name'],
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('siglum', models.CharField(unique=True, max_length=15, verbose_name='Siglum')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('logo', models.URLField(null=True, verbose_name='Logo', blank=True)),
                ('wikipedia', models.URLField(null=True, verbose_name='Wikipedia', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Education',
                'verbose_name_plural': 'Educations',
            },
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField(unique=True, verbose_name='Year')),
            ],
            options={
                'ordering': ['-year'],
                'verbose_name': 'Election',
                'verbose_name_plural': 'Elections',
            },
        ),
        migrations.CreateModel(
            name='ElectionRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.CharField(max_length=1, verbose_name='Round', choices=[(b'1', 'Round 1'), (b'2', 'Round 2')])),
                ('date', models.DateField(verbose_name='Date')),
                ('election', models.ForeignKey(related_name='rounds', to='politicians.Election')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Election Round',
                'verbose_name_plural': 'Election Rounds',
            },
        ),
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Ethnicity',
                'verbose_name_plural': 'Ethnicities',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('siglum', models.CharField(max_length=10, verbose_name='Siglum')),
                ('logo', models.URLField(null=True, verbose_name='Logo', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('wikipedia', models.URLField(null=True, verbose_name='Wikipedia', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
            },
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(help_text='Date in which this mandate started; may also be a resumption of a mandate that was paused for taking an executive-branch office, or a party change.', verbose_name='Date Started', db_index=True)),
                ('date_end', models.DateField(help_text='Date in which this mandate ended, paused for taking an executive-branch office, or affiliation change.', null=True, verbose_name='Date Ended', db_index=True, blank=True)),
                ('candidacy', models.ForeignKey(to='politicians.Candidacy')),
            ],
            options={
                'ordering': ['date_start', 'candidacy__politician__name'],
                'verbose_name': 'Mandate',
                'verbose_name_plural': 'Mandates',
            },
        ),
        migrations.CreateModel(
            name='MandateEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Date', db_index=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('mandate', models.ForeignKey(related_name='mandates', to='politicians.Mandate')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Mandate Event',
                'verbose_name_plural': 'Mandate Events',
            },
        ),
        migrations.CreateModel(
            name='MandateEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Mandate Event Type',
                'verbose_name_plural': 'Mandate Event Types',
            },
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Full Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Marital Status',
                'verbose_name_plural': 'Marital Status',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Nationality',
                'verbose_name_plural': 'Nationalities',
            },
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Occupation',
                'verbose_name_plural': 'Occupations',
            },
        ),
        migrations.CreateModel(
            name='PoliticalOffice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('term', models.IntegerField(verbose_name='Term')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('wikipedia', models.URLField(null=True, verbose_name='Wikipedia', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Political Office',
                'verbose_name_plural': 'Political Offices',
            },
        ),
        migrations.CreateModel(
            name='PoliticalParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('siglum', models.CharField(unique=True, max_length=15, verbose_name='Siglum')),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Full Name')),
                ('wikipedia', models.URLField(null=True, verbose_name='Wikipedia', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('logo', models.URLField(null=True, verbose_name='Logo', blank=True)),
                ('founded_date', models.DateField(null=True, verbose_name='Founded Date', blank=True)),
                ('tse_number', models.IntegerField(null=True, verbose_name='TSE Number', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Political Party',
                'verbose_name_plural': 'Political Parties',
            },
        ),
        migrations.CreateModel(
            name='Politician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('cpf', models.CharField(unique=True, max_length=11, verbose_name='CPF')),
                ('picture', models.URLField(null=True, verbose_name='Picture', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True)),
                ('about', models.TextField(null=True, verbose_name='About', blank=True)),
                ('gender', models.CharField(choices=[(b'F', 'Female'), (b'M', 'Male')], max_length=1, blank=True, null=True, verbose_name='Gender', db_index=True)),
                ('date_of_birth', models.DateField(null=True, verbose_name='Date of Birth', blank=True)),
                ('place_of_birth', models.CharField(max_length=255, null=True, verbose_name='Place of Birth', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Politician',
                'verbose_name_plural': 'Politicians',
            },
        ),
        migrations.CreateModel(
            name='PoliticianAlternativeName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Politician Alternative Name',
                'verbose_name_plural': 'Politician Alternative Names',
            },
        ),
        migrations.CreateModel(
            name='PoliticianEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='Date', db_index=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('politician', models.ForeignKey(related_name='politicians_events', to='politicians.Politician')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'Politician Event',
                'verbose_name_plural': 'Politician Events',
            },
        ),
        migrations.CreateModel(
            name='PoliticianEventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Politician Event Type',
                'verbose_name_plural': 'Politician Event Types',
            },
        ),
        migrations.CreateModel(
            name='PoliticianPoliticalParty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_start', models.DateField(help_text='Date in which this politician started.', null=True, verbose_name='Date Started', db_index=True, blank=True)),
                ('date_end', models.DateField(help_text='Date in which this politician ended.', null=True, verbose_name='Date Ended', db_index=True, blank=True)),
                ('political_party', models.ForeignKey(to='politicians.PoliticalParty')),
                ('politician', models.ForeignKey(related_name='politicians', to='politicians.Politician')),
            ],
            options={
                'ordering': ['political_party'],
                'verbose_name': 'Politician Political Party',
                'verbose_name_plural': 'Politician Political Parties',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('siglum', models.CharField(unique=True, max_length=15, verbose_name='Siglum')),
                ('slug', models.SlugField(unique=True, max_length=255, verbose_name='Slug')),
                ('logo', models.URLField(null=True, verbose_name='Logo', blank=True)),
                ('wikipedia', models.URLField(null=True, verbose_name='Wikipedia', blank=True)),
                ('country', models.ForeignKey(to='politicians.Country')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.AddField(
            model_name='politicianevent',
            name='politician_event_type',
            field=models.ForeignKey(to='politicians.PoliticianEventType'),
        ),
        migrations.AddField(
            model_name='politician',
            name='alternative_names',
            field=models.ManyToManyField(to='politicians.PoliticianAlternativeName', verbose_name='Alternative Names', blank=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='education',
            field=models.ForeignKey(blank=True, to='politicians.Education', null=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='ethnicity',
            field=models.ForeignKey(blank=True, to='politicians.Ethnicity', null=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='marital_status',
            field=models.ForeignKey(blank=True, to='politicians.MaritalStatus', null=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='nationality',
            field=models.ForeignKey(blank=True, to='politicians.Nationality', null=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='occupation',
            field=models.ForeignKey(blank=True, to='politicians.Occupation', null=True),
        ),
        migrations.AddField(
            model_name='politician',
            name='state',
            field=models.ForeignKey(blank=True, to='politicians.State', null=True),
        ),
        migrations.AddField(
            model_name='mandateevent',
            name='mandate_event_type',
            field=models.ForeignKey(to='politicians.MandateEventType'),
        ),
        migrations.AddField(
            model_name='institution',
            name='political_offices',
            field=models.ManyToManyField(to='politicians.PoliticalOffice', verbose_name='Political Offices', blank=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='state',
            field=models.ForeignKey(blank=True, to='politicians.State', null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(to='politicians.State'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='candidacy_status',
            field=models.ForeignKey(to='politicians.CandidacyStatus'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='city',
            field=models.ForeignKey(blank=True, to='politicians.City', null=True),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='election_round',
            field=models.ForeignKey(to='politicians.ElectionRound'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='institution',
            field=models.ForeignKey(to='politicians.Institution'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='political_office',
            field=models.ForeignKey(to='politicians.PoliticalOffice'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='politician',
            field=models.ForeignKey(to='politicians.Politician'),
        ),
        migrations.AddField(
            model_name='candidacy',
            name='state',
            field=models.ForeignKey(blank=True, to='politicians.State', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='mandate',
            unique_together=set([('candidacy', 'date_start', 'date_end')]),
        ),
        migrations.AlterUniqueTogether(
            name='institution',
            unique_together=set([('name', 'state')]),
        ),
        migrations.AlterUniqueTogether(
            name='electionround',
            unique_together=set([('election', 'round_number')]),
        ),
    ]
