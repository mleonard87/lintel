from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=255)
    support_telephone = models.CharField(max_length=100)
    welcome_message = models.CharField(max_length=255)

    def get_shifts(self):
        return self.shift_set.all().order_by('user')

    def get_on_duty_shifts(self):
        now = timezone.now()
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

class CallLog(models.Model):
    call_sid = models.CharField(max_length=100)
    to_telephone = models.CharField(max_length=100)
    from_telephone = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True)
    support_agent = models.ForeignKey(SupportAgent, null=True)

    def get_project_display(self):
        display_text = ''
        try:
            project = Project.objects.get(support_telephone=self.to_telephone)
            display_text = project.title
        except Project.DoesNotExist:
            display_text = ''

        return display_text

    def get_telephone_display(self, telephone):
        display_text = ''
        try:
            support_agent = SupportAgent.objects.get(telephone=telephone)
            display_text = support_agent.user.get_full_name()
        except SupportAgent.DoesNotExist:
            display_text = telephone

        return display_text

    def get_to_telephone_display(self):
        return self.get_telephone_display(self.to_telephone)

    def get_from_telephone_display(self):
        return self.get_telephone_display(self.from_telephone)

    def get_duration_display(self):
        if not self.end_datetime:
            return '-'
        else:
            dt = self.end_datetime - self.start_datetime
            seconds = dt.seconds
            if seconds >= 60:
                return '%d min %d sec' % (seconds / 60, seconds % 60)
            else:
                return '0 min %d sec' % seconds

    def __unicode__(self):
        return '%s %s - %s' % (self.support_agent.user, self.start_datetime, self.end_datetime)
