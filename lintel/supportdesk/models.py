from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime

class Project(models.Model):
    title = models.CharField(max_length=255)
    support_telephone = models.CharField(max_length=100)
    welcome_message = models.CharField(max_length=255)

    def get_shifts(self):
        return self.shift_set.all().order_by('user')

    def get_on_duty_shifts(self):
        now = datetime.datetime.now()
        today_code = now.strftime('%a').upper()

        return self.shift_set.filter(
            day=today_code,
            start__lt=now.time(),
            end__gt=now.time()
        )

    def __unicode__(self):
        return self.title

class Shift(models.Model):
    DAYS = (
      ('MON', 'Monday'),
      ('TUE', 'Tuesday'),
      ('WED', 'Wednesday'),
      ('THU', 'Thursday'),
      ('FRI', 'Friday'),
      ('SAT', 'Saturday'),
      ('SUN', 'Sunday'),
    )

    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    day = models.CharField(max_length=20, choices=DAYS)
    start = models.TimeField()
    end = models.TimeField()

    def __unicode__(self):
        return '%s: %s %s-%s' % (self.user, self.day, self.start, self.end)

class SupportAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=100)

    def get_shifts(self):
        return Shift.objects.filter(user=self.user)

    def __unicode__(self):
        return self.user.get_full_name
