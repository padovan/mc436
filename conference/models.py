from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):

    area = models.CharField(max_length=256)
    description = models.CharField(max_length=2048)

    def __unicode__(self):
        return self.area


class SiteUser(User):

    cpf = models.CharField(max_length=14)
    organization = models.CharField(max_length=256)
    newsletter = models.BooleanField()
    #FIXME: we will not implement this now
    #email_verified = models.BooleanField()

    def __unicode__(self):
        return self.username


class SponsorType(models.Model):

    interesting = models.ManyToManyField(Area)
    name = models.CharField(max_length=256)
    amount = models.PositiveIntegerField()
    max_invites = models.SmallIntegerField()

    def __unicode__(self):
        return self.name


class Sponsor(SiteUser):

    name = models.CharField(max_length=256)
    type = models.ForeignKey(SponsorType)
    # just for convenience, we can count all invited instead
    num_invited = models.SmallIntegerField()

    def __unicode__(self):
        return self.name


class Participant(SiteUser):

    invited = models.BooleanField(default=False)
    sponsor = models.ForeignKey(Sponsor)

    def __unicode__(self):
        return self.username


class Speaker(Participant):

    # FIXME: We are using Char field to represent a File field (i.e. 'migueh')
    cv = models.CharField(max_length=65536)

    def __unicode__(self):
        return self.username


class Reviewer(Participant):

    status = models.BooleanField()

    def __unicode__(self):
        return self.username


class Text(models.Model):

    title = models.CharField(max_length=256)
    # FIXME: We are using Char field to represent a File field (i.e. 'migueh')
    content = models.CharField(max_length=65536)
    area = models.ManyToManyField(Area)
    type = models.BooleanField()
    author = models.ForeignKey(SiteUser)
    #FIXME: we really need this optimization?
    num_reviewers = models.PositiveSmallIntegerField()
    reviewer = models.ManyToManyField(Reviewer, related_name="reviewer_text")
    # reviewed just for convenience, if false we need to search if all
    # reviewers already reviewed the text
    reviewed = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class ConferenceSettings(models.Model):
    max_reviewers = models.PositiveIntegerField()

    def __unicode__(self):
        return None

