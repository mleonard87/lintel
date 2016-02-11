from django.conf.urls import patterns, url

urlpatterns = patterns('supportdesk.views',
    url(r'projects/$', 'projects', name='projects'),
    url(r'projects/(?P<project_id>[0-9]*)/$', 'projects_manage', name='projects_manage'),
    url(r'projects/new/$', 'projects_new', name='projects_new'),
    url(r'people/$', 'support_agents', name='support_agents'),
    url(r'people/(?P<support_agent_id>[0-9]*)/$', 'support_agents_manage', name='support_agents_manage'),
    url(r'people/new/$', 'support_agents_new', name='support_agents_new'),
    url(r'calls/$', 'calls', name='calls'),
    url(r'reporting/$', 'projects', name='reporting'),
    url(r'^$', 'dashboard', name='dashboard'),
)
