from django.conf.urls import patterns, url

urlpatterns = patterns('twilioapi.views',
    url(r'begin/$', 'begin_call', name='twilio_begin_call'),
    url(r'complete/$', 'complete_call', name='twilio_complete_call'),
)
