# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2013, Gustavo Noronha Silva
# Copyright (c) 2015, Marcelo Jorge Vieira <metal@alucinados.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify


class Country(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    siglum = models.CharField(
        max_length=15,
        verbose_name=_('Siglum'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    logo = models.URLField(
        verbose_name=_('Logo'),
        blank=True,
        null=True,
    )

    wikipedia = models.URLField(
        verbose_name=_('Wikipedia'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)


class State(models.Model):

    country = models.ForeignKey('Country')

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    siglum = models.CharField(
        max_length=15,
        verbose_name=_('Siglum'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    logo = models.URLField(
        verbose_name=_('Logo'),
        blank=True,
        null=True,
    )

    wikipedia = models.URLField(
        verbose_name=_('Wikipedia'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(State, self).save(*args, **kwargs)


class City(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        db_index=True,
    )

    state = models.ForeignKey('State')

    logo = models.URLField(
        verbose_name=_('Logo'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['state', 'name']

    def __unicode__(self):
        return u'{0}'.format(self.name)


class ElectionRound(models.Model):

    election = models.ForeignKey('Election',  related_name='rounds')

    round_number = models.CharField(
        verbose_name=_('Round'),
        choices=(
            ('1', _('Round 1')),
            ('2', _('Round 2')),
        ),
        max_length=1,
    )

    date = models.DateField(verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Election Round')
        verbose_name_plural = _('Election Rounds')
        ordering = ['date']
        unique_together = ('election', 'round_number')

    def __unicode__(self):
        return u'{0}: {1}'.format(
            self.round_number,
            self.date.strftime('%Y-%m-%d'),
        )


class Election(models.Model):

    year = models.IntegerField(
        verbose_name=_('Year'),
        unique=True,
    )

    class Meta:
        verbose_name = _('Election')
        verbose_name_plural = _('Elections')
        ordering = ['-year']

    def __unicode__(self):
        return u'{0}'.format(self.year)


class PoliticalParty(models.Model):

    siglum = models.CharField(
        max_length=15,
        verbose_name=_('Siglum'),
        unique=True,
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Full Name'),
        unique=True,
    )

    wikipedia = models.URLField(
        verbose_name=_('Wikipedia'),
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        blank=True,
        null=True,
    )

    logo = models.URLField(
        verbose_name=_('Logo'),
        blank=True,
        null=True,
    )

    founded_date = models.DateField(
        verbose_name=_('Founded Date'),
        blank=True,
        null=True,
    )

    tse_number = models.IntegerField(
        verbose_name=_('TSE Number'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Political Party')
        verbose_name_plural = _('Political Parties')
        ordering = ['name']

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.siglum)

    @classmethod
    def get_by_siglum(self, siglum):
        try:
            return PoliticalParty.objects.cache().get(siglum=siglum)
        except PoliticalParty.DoesNotExist:
            return None

    @classmethod
    def get_by_name(self, name):
        try:
            return PoliticalParty.objects.cache().get(name=name)
        except PoliticalParty.DoesNotExist:
            return None


class Institution(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
    )

    siglum = models.CharField(
        max_length=10,
        verbose_name=_('Siglum'),
    )

    logo = models.URLField(
        verbose_name=_('Logo'),
        blank=True,
        null=True,
    )

    state = models.ForeignKey('State', blank=True, null=True)

    website = models.URLField(
        verbose_name=_('Website'),
        blank=True,
        null=True,
    )

    wikipedia = models.URLField(
        verbose_name=_('Wikipedia'),
        blank=True,
        null=True,
    )

    political_offices = models.ManyToManyField(
        'PoliticalOffice',
        verbose_name=_('Political Offices'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Institution')
        verbose_name_plural = _('Institutions')
        ordering = ['name']
        unique_together = ('name', 'state')

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.siglum)

    @classmethod
    def get_by_political_office_name(self, name):
        return Institution.objects.filter(political_offices__name=name).cache()

    @classmethod
    def get_by_political_office_name_and_state(self, name, state):
        try:
            if state:
                return Institution.objects.cache().get(
                    political_offices__name=name,
                    state=state,
                )
            else:
                return Institution.objects.cache().get(
                    political_offices__name=name,
                )
        except Institution.DoesNotExist:
            return None


class PoliticianPoliticalParty(models.Model):

    politician = models.ForeignKey('Politician', related_name='politicians')

    political_party = models.ForeignKey('PoliticalParty')

    date_start = models.DateField(
        verbose_name=_('Date Started'),
        help_text=_('Date in which this politician started.'),
        db_index=True,
        blank=True,
        null=True,
    )

    date_end = models.DateField(
        verbose_name=_('Date Ended'),
        help_text=_('Date in which this politician ended.'),
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Politician Political Party')
        verbose_name_plural = _('Politician Political Parties')
        ordering = ['political_party']

    def __unicode__(self):
        return u'{0}: {1}'.format(self.politician, self.political_party)


class PoliticianAlternativeName(models.Model):

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _('Politician Alternative Name')
        verbose_name_plural = _('Politician Alternative Names')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Education(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Ethnicity(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Ethnicity')
        verbose_name_plural = _('Ethnicities')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Ethnicity, self).save(*args, **kwargs)


class MaritalStatus(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Full Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Marital Status')
        verbose_name_plural = _('Marital Status')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(MaritalStatus, self).save(*args, **kwargs)


class Nationality(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationalities')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Nationality, self).save(*args, **kwargs)


class Occupation(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Occupation')
        verbose_name_plural = _('Occupations')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Occupation, self).save(*args, **kwargs)


class Politician(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Full Name'),
    )

    cpf = models.CharField(
        verbose_name=_('CPF'),
        max_length=11,
        unique=True,
    )

    picture = models.URLField(
        verbose_name=_('Picture'),
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email'),
        blank=True,
        null=True,
    )

    about = models.TextField(
        verbose_name=_('About'),
        blank=True,
        null=True,
    )

    gender = models.CharField(
        verbose_name=_('Gender'),
        choices=(
            ('F', _('Female')),
            ('M', _('Male')),
        ),
        blank=True,
        null=True,
        max_length=1,
        db_index=True,
    )

    ethnicity = models.ForeignKey(
        'Ethnicity',
        blank=True,
        null=True,
    )

    education = models.ForeignKey(
        'Education',
        blank=True,
        null=True,
    )

    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth'),
        blank=True,
        null=True,
    )

    marital_status = models.ForeignKey(
        'MaritalStatus',
        blank=True,
        null=True,
    )

    nationality = models.ForeignKey(
        'Nationality',
        blank=True,
        null=True,
    )

    state = models.ForeignKey(
        'State',
        blank=True,
        null=True,
    )

    place_of_birth = models.CharField(
        verbose_name=_('Place of Birth'),
        max_length=255,
        blank=True,
        null=True,
    )

    occupation = models.ForeignKey(
        'Occupation',
        blank=True,
        null=True,
    )

    alternative_names = models.ManyToManyField(
        'PoliticianAlternativeName',
        verbose_name=_('Alternative Names'),
        blank=True,
    )

    class Meta:
        verbose_name = _('Politician')
        verbose_name_plural = _('Politicians')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)


class CandidacyStatus(models.Model):

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Candidacy Status')
        verbose_name_plural = _('Candidacies Status')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Candidacy(models.Model):

    election_round = models.ForeignKey('ElectionRound')

    politician = models.ForeignKey('Politician', related_name='candidacies')

    elected = models.BooleanField(verbose_name=_('Elected'))

    state = models.ForeignKey('State', blank=True, null=True)

    city = models.ForeignKey('City', blank=True, null=True)

    political_office = models.ForeignKey('PoliticalOffice')

    candidacy_status = models.ForeignKey('CandidacyStatus')

    institution = models.ForeignKey('Institution')

    class Meta:
        verbose_name = _('Candidacy')
        verbose_name_plural = _('Candidacies')
        ordering = [
            'election_round__election__year',
            'election_round',
            'politician__name',
        ]

    def __unicode__(self):
        return u'{0}: {1}/{2}'.format(
            self.politician, self.election_round.election.year,
            self.election_round.round_number
        )


class PoliticianEventType(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Politician Event Type')
        verbose_name_plural = _('Politician Event Types')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(PoliticianEventType, self).save(*args, **kwargs)


class PoliticianEvent(models.Model):

    politician = models.ForeignKey(
        'Politician',
        related_name='politicians_events'
    )

    politician_event_type = models.ForeignKey('PoliticianEventType')

    date = models.DateField(
        verbose_name=_('Date'),
        db_index=True,
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Politician Event')
        verbose_name_plural = _('Politician Events')
        ordering = ['date']

    def __unicode__(self):
        return u'{0}: {1}'.format(
            self.date.strftime('%Y-%m-%d'), self.politician_event_type.name
        )


class PoliticalOffice(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    term = models.IntegerField(verbose_name=_('Term'))

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    wikipedia = models.URLField(
        verbose_name=_('Wikipedia'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Political Office')
        verbose_name_plural = _('Political Offices')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @classmethod
    def get_by_name(self, name):
        try:
            return PoliticalOffice.objects.cache().get(name=name)
        except PoliticalOffice.DoesNotExist:
            return None

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(PoliticalOffice, self).save(*args, **kwargs)


class MandateEventType(models.Model):

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        unique=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = _('Mandate Event Type')
        verbose_name_plural = _('Mandate Event Types')
        ordering = ['name']

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(MandateEventType, self).save(*args, **kwargs)


class MandateEvent(models.Model):

    mandate = models.ForeignKey('Mandate', related_name='mandates')

    mandate_event_type = models.ForeignKey('MandateEventType')

    date = models.DateField(
        verbose_name=_('Date'),
        db_index=True,
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Mandate Event')
        verbose_name_plural = _('Mandate Events')
        ordering = ['date']

    def __unicode__(self):
        return u'{0}: {1}'.format(
            self.date.strftime('%Y-%m-%d'), self.mandate_event_type.name
        )


class Mandate(models.Model):

    candidacy = models.ForeignKey('Candidacy')

    date_start = models.DateField(
        verbose_name=_('Date Started'),
        help_text=_(
            'Date in which this mandate started; may also be '
            'a resumption of a mandate that was paused for taking '
            'an executive-branch office, or a party change.'
        ),
        db_index=True,
    )

    date_end = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date Ended'),
        help_text=_(
            'Date in which this mandate ended, paused for taking an '
            'executive-branch office, or affiliation change.'
        ),
        db_index=True,
     )

    class Meta:
        verbose_name = _('Mandate')
        verbose_name_plural = _('Mandates')
        ordering = ['date_start', 'candidacy__politician__name']
        unique_together = ('candidacy', 'date_start', 'date_end')

    def __unicode__(self):
        if not self.date_end:
            return u'{0}\'s ongoing mandate started on {1}'.format(
                self.candidacy.politician.name,
                self.date_start.strftime('%Y-%m-%d'),
            )

        return u'{0}\'s mandate started on {1} ended on {2}'.format(
            self.candidacy.politician.name,
            self.date_start.strftime('%Y-%m-%d'),
            self.date_end.strftime('%Y-%m-%d'),
        )
