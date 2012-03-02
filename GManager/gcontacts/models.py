# -*- coding: utf-8 -*-

from django.db import models


class SyncUser(models.Model):
    email = models.CharField(u'E-Mail',max_length=255)
    pwd = models.CharField(u'Passwort',max_length=100)
    active = models.BooleanField(u'Syncronisieren',default=True)

    def __unicode__(self):
        return self.email

class Contact(models.Model):
    origin = models.ForeignKey(SyncUser)
    firstname = models.CharField(u'Vorname', max_length=255)
    lastname = models.CharField(u'Nachname',max_length=255)
    prname = models.CharField(u'Vorsilbe',max_length=100, null=True)
    suname = models.CharField(u'Endsilbe',max_length=100, null=True)
    addname = models.CharField(u'Zweiter Vorname',max_length=255, null=True)
    email = models.CharField(u'E-Mail',max_length=255, null=True)
    phone = models.CharField(u'Telefon',max_length=255, null=True)
    street = models.CharField(u'Straße',max_length=255, null=True)
    pob = models.CharField(u'Postfach',max_length=20, null=True)
    zip = models.CharField(u'Postleitzahl',max_length=10, null=True)
    city = models.CharField(u'Stadt',max_length=255, null=True)
    state = models.CharField(u'Bundesland',max_length=255, null=True)
    country = models.CharField(u'Land',max_length=255, null=True)
    bday = models.DateField(u'Geburtstag', null=True)
    website = models.CharField(u'Website',max_length=255, null=True)

    def __unicode__(self):
        return self.firstname + "" + self.lastname
